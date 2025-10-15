from rotary_irq_rp2 import RotaryIRQ # type: ignore
from machine import Pin

# next pattern
side_btn = Pin.cpu.GPIO13
side_down = False

# speed/intensity
side_rot = RotaryIRQ(
  pin_num_clk=11,
  pin_num_dt=12,
  min_val=1,
  max_val=100,
  incr=5,
  reverse=True,
  range_mode=RotaryIRQ.RANGE_BOUNDED
)
side_rot.set(value=50)
side_rot.add_listener(lambda: print('side', side_rot.value()))

# prev pattern
front_btn = Pin.cpu.GPIO18
front_down = False

# brightness
front_rot = RotaryIRQ(
  pin_num_clk=20,
  pin_num_dt=19,
  min_val=1,
  max_val=255,
  incr=16,
  reverse=True,
  range_mode=RotaryIRQ.RANGE_BOUNDED
)
front_rot.set(value=128)
front_rot.add_listener(lambda: print('front', front_rot.value()))
