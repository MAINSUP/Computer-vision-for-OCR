import layoutparser as lp
import numpy as np
import warnings
warnings.filterwarnings('ignore')


def layout_parser(page, blockconfidence):
    model = lp.models.Detectron2LayoutModel('lp://PubLayNet/faster_rcnn_R_50_FPN_3x/config',
                                            extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", blockconfidence],
                                            label_map={0: "Text", 1: "Title", 2: "List", 3: "Table", 4: "Figure"},
                                            device='cpu')
    # Load the deep layout model from the layoutparser API
    # For all the supported model, please check the Model Zoo
    # Page: https://layout-parser.readthedocs.io/en/latest/notes/modelzoo.html
    layout = model.detect(page[..., ::-1])
    # Detect the layout of the input image
    # lp.draw_box(page[..., ::-1], layout, box_width=3)  # Show the detected layout of the input image
    text_blocks = lp.Layout([b for b in layout if b.type == 'Text'])
    title_blocks = lp.Layout([b for b in layout if b.type == 'Title'])
    figure_blocks = lp.Layout([b for b in layout if b.type == 'Figure'])
    h, w = page.shape[:2]
    left_interval = lp.Interval(0, w / 2 * 1.05, axis='x').put_on_canvas(page)
    left_blocks = title_blocks.filter_by(left_interval, center=True) + text_blocks.filter_by(left_interval, center=True)
    left_blocks.sort(key=lambda b: b.coordinates[1], inplace=True)
    # The b.coordinates[1] corresponds to the y coordinate of the region
    # sort based on that can simulate the top-to-bottom reading order
    right_blocks = lp.Layout([b for b in title_blocks if b not in left_blocks] +
                             [b for b in text_blocks if b not in left_blocks])
    right_blocks.sort(key=lambda b: b.coordinates[1], inplace=True)

    # And finally combine the two lists and add the index
    if len(figure_blocks) > 0:
        figure_block = fig_block(figure_blocks, layout)
        text_blocks = lp.Layout([b.set(id=idx) for idx, b in enumerate(lp.Layout(figure_block) +
                                                                       left_blocks +
                                                                       right_blocks)])
        text_blocks.sort(key = lambda b:b.coordinates[1], inplace=True)
    else:
        text_blocks = lp.Layout([b.set(id=idx) for idx, b in enumerate(left_blocks + right_blocks)])
        text_blocks.sort(key = lambda b:b.coordinates[1], inplace=True)
    textim_arr = []
    for block in text_blocks:
        segment_image = (block
                         .pad(left=10, right=10, top=26, bottom=30)
                         .crop_image(page))
        # add padding in each image segment can help improve robustness
        textim_arr.append(segment_image)

    return textim_arr


def fig_block(figure_blocks, layout):   # utility function that may utilize figure block OCR;
    area = []                           # in case few fiure blocks overlap, function would detect the largest one
    for i in range(len(figure_blocks)):                                                           # for processing
        coor = list(lp.Layout([b for b in layout if b.type == 'Figure'])[i].coordinates)
        area.append((coor[2] - coor[0]) * (coor[3] - coor[1]))
    figure_block = [figure_blocks[np.argmax(area)]]
    for i, block in enumerate(figure_blocks):
        dx = min(int(figure_blocks[i].block.x_2), int(figure_blocks[np.argmax(area)].block.x_2)) - max(
            int(figure_blocks[i].block.x_1), int(figure_blocks[np.argmax(area)].block.x_1))
        dy = min(int(figure_blocks[i].block.y_2), int(figure_blocks[np.argmax(area)].block.y_2)) - max(
            int(figure_blocks[i].block.y_1), int(figure_blocks[np.argmax(area)].block.y_1))
        if (dx > 0) and (dy >= 0):
            pass
        else:
            figure_block.append(block)
        return figure_block
