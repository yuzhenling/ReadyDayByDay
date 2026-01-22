import minimalmodbus
import serial
import time

# 启用调试模式（可查看报文交互细节）
minimalmodbus.DEBUG = False  # 如需调试可改为True


def init_instrument():
    """初始化仪器连接，配置协议参数"""
    instrument = minimalmodbus.Instrument(
        port='/dev/ttyS6',  # 串口号根据实际设备修改
        slaveaddress=1,  # 从机地址（默认1，可通过协议0x0000地址修改）
        mode=minimalmodbus.MODE_RTU  # 协议规定为RTU模式
    )
    # 配置串口参数（协议"串行数据格式"规定）
    instrument.serial.baudrate = 9600  # 波特率，可通过0x0001地址修改
    instrument.serial.bytesize = 8  # 8位数据位
    instrument.serial.parity = serial.PARITY_NONE  # 无校验
    instrument.serial.stopbits = 1  # 1位停止位
    instrument.serial.timeout = 1.0  # 超时时间1秒
    instrument.retries = 2  # 读取失败重试次数
    return instrument


def parse_measured_value(raw_value, decimal_point):
    """根据协议解析测量值（整数→浮点数）"""
    if decimal_point not in [0, 1, 2, 3]:
        return None, "无效小数点位数（协议规定0-3）"
    try:
        # 协议规定：浮点数=整数/10^小数点位数，负值用补码表示
        parsed = raw_value / (10 ** decimal_point)
        return parsed, "解析成功"
    except Exception as e:
        return None, f"解析失败：{str(e)}"


def read_transmitter_data(instrument):
    """读取一次变送器数据（按协议寄存器地址读取）"""
    try:
        # 1. 读取测量输出值（协议0x0004地址，功能码0x03）
        measured_raw = instrument.read_register(
            registeraddress=0x0004,
            functioncode=3,
            signed=True  # 支持负值（补码形式）
        )

        # 2. 读取小数点位数（协议0x0003地址，用于解析浮点数）
        decimal_point = instrument.read_register(
            registeraddress=0x0003,
            functioncode=3
        )

        # 3. 读取压力单位（协议0x0002地址，映射单位名称）
        unit_code = instrument.read_register(
            registeraddress=0x0002,
            functioncode=3
        )
        unit_map = {  # 协议"压力单位"列表映射
            0: "Mpa/℃", 1: "Kpa", 2: "Pa", 3: "Bar",
            4: "Mbar", 5: "kg/cm²", 6: "psi", 7: "mh2o", 8: "mmh2o"
        }
        unit = unit_map.get(unit_code, f"未知单位（代码：{unit_code}）")

        # 解析测量值
        parsed_value, parse_msg = parse_measured_value(measured_raw, decimal_point)
        if parsed_value is not None:
            return {
                "原始值": measured_raw,
                "解析值": f"{parsed_value} {unit}",
                "状态": "正常"
            }
        else:
            return {"状态": f"解析错误：{parse_msg}"}

    except minimalmodbus.ModbusException as e:
        return {"状态": f"Modbus协议错误：{str(e)}（参考协议异常应答码）"}
    except Exception as e:
        return {"状态": f"读取失败：{str(e)}"}


def loop_read(interval=1):
    """循环读取，每秒一次（严格控制间隔）"""
    instrument = None
    try:
        instrument = init_instrument()
        print("开始循环读取（每秒1次），按Ctrl+C停止...")
        while True:
            start_time = time.time()
            data = read_transmitter_data(instrument)
            print(f"[{time.strftime('%H:%M:%S')}] {data}")
            # 控制循环间隔（扣除读取耗时，确保约1秒一次）
            elapsed = time.time() - start_time
            if elapsed < interval:
                time.sleep(interval - elapsed)
    except KeyboardInterrupt:
        print("\n用户终止循环")
    finally:
        if instrument:
            instrument.serial.close()
            print("串口已关闭")


if __name__ == "__main__":
    loop_read()