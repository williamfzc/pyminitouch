from pyminitouch import safe_connection, CommandBuilder

_DEVICE_ID = "123456F"


with safe_connection(_DEVICE_ID) as connection:
    builder = CommandBuilder()
    builder.down(0, 400, 800, 50)
    builder.commit()
    builder.move(0, 0, 400, 50)
    builder.commit()
    builder.move(0, 200, 200, 50)
    builder.commit()
    builder.move(0, 400, 400, 50)
    builder.commit()
    builder.move(0, 600, 200, 50)
    builder.commit()
    builder.move(0, 800, 400, 50)
    builder.commit()
    builder.move(0, 400, 800, 50)
    builder.commit()

    builder.up(0)
    builder.commit()

    builder.publish(connection)
