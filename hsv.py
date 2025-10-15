
def to_rgb(h, s, v):
  if s == 0:
    return (v, v, v)

  h = h % 360
  x = h // 60
  f = (h % 60) * 255 // 60

  p = (v * (255 - s)) // 255
  q = (v * (255 - (s * f) // 255)) // 255
  t = (v * (255 - (s * (255 - f) // 255))) // 255

  if x == 0:
    return (v, t, p)
  elif x == 1:
    return (q, v, p)
  elif x == 2:
    return (p, v, t)
  elif x == 3:
    return (p, q, v)
  elif x == 4:
    return (t, p, v)
  else:
    return (v, p, q)
