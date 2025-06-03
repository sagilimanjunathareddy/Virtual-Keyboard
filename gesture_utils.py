def is_pinch(index_tip, thumb_tip):
    ix, iy = index_tip
    tx, ty = int(thumb_tip[0] * 640), int(thumb_tip[1] * 480)
    dist = ((ix - tx) ** 2 + (iy - ty) ** 2) ** 0.5
    return dist < 40
