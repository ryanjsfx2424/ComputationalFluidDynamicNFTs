import asyncio

## tested if memory is shared (it is!)
class Test(object):
  def __init__(self):
    self.value = 0

  async def set_value(self, value):
    for ii in range(1000):
      self.value = value
      print("sv: ", value)
      await asyncio.sleep(0.2)

  async def loop(self):
    for value in range(3,1000):
      await asyncio.sleep(0.2)
      print("loop: ", value)

  async def print_value(self):
    await asyncio.sleep(0.2)
    print("self.value: ", self.value)

  async def set_and_print_value(self, value):
    await self.set_value(value)
    await self.print_value()
# end class

async def main():
  test_instance = Test()

  await test_instance.print_value()
  await asyncio.gather(
        test_instance.print_value(),
        test_instance.set_and_print_value(2),
        test_instance.set_value(1),
        test_instance.loop()
                      )

asyncio.run(main())
