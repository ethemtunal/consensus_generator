from numpy import percentile


def get_iou(box1, box2):
    # determine the (x, y)-coordinates of the intersection rectangle
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    # compute the area of intersection rectangle
    inter_area = abs(max((x2 - x1, 0)) * max((y2 - y1), 0))
    if inter_area == 0:
        return 0
    # compute the area of both the prediction and ground-truth
    # rectangles
    box1_area = abs((box1[2] - box1[0]) * (box1[3] - box1[1]))
    box2_area = abs((box2[2] - box2[0]) * (box2[3] - box2[1]))

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the intersection area
    iou = inter_area / float(box1_area + box2_area - inter_area)

    # return the intersection over union value
    return iou * 10


def get_valid_range(coordinates):
    q1, q3 = percentile(sorted(coordinates), [25, 75])
    iqr = q3 - q1
    upper_bound = q3 + (1.5 * iqr)
    lower_bound = q1 - (1.5 * iqr)
    return {"lower": lower_bound, "upper": upper_bound}


def is_invalid_range(coordinates):
    bounds = get_valid_range(coordinates)
    upper = coordinates >= bounds["upper"]
    lower = coordinates <= bounds["lower"]
    result = [i or j for i, j in zip(upper, lower)]
    return result


def get_non_valid(boxes):
    x1s = is_invalid_range([b["box"][0] for b in boxes])
    y1s = is_invalid_range([b["box"][1] for b in boxes])
    x2s = is_invalid_range([b["box"][2] for b in boxes])
    y2s = is_invalid_range([b["box"][3] for b in boxes])
    annotation_ids = [b["annotation"] for b in boxes]
    result = {a: [i, j, k, l] for a, i, j, k, l in zip(annotation_ids, x1s, y1s, x2s, y2s)}
    return result
