import logging

from gkg_laser.laser_client import DazuLaserMarkerClient
from gkg_laser.laser_command import LaserCommand


class LaserController:
    """激光打标机控制封装类"""

    def __init__(self, host: str, port: int):
        self.client = DazuLaserMarkerClient(host, port)
        self.logger = logging.getLogger("LaserController")

    def execute_command(self, command: LaserCommand, payload: str = "") -> bool:
        """执行激光控制指令

        Args:
            command: 枚举指令类型
            payload: 附加参数（例如："power=80,x=100,y=200"）

        Returns:
            bool: 是否执行成功
        """
        try:
            # 构造完整指令
            full_command = f"{command.send}{payload}"

            # 发送指令并等待响应
            response = self.client.send_command(full_command, wait_response=True)

            # 验证响应
            if response == command.success:
                self.logger.info(f"{command.name} 操作成功")
                return True
            elif response == command.fail:
                self.logger.error(f"{command.name} 操作失败")
                return False
            else:
                self.logger.warning(f"收到未知响应: {response}")
                return False
        except TimeoutError:
            self.logger.error(f"{command.name} 操作超时")
            return False
        except Exception as e:
            self.logger.error(f"{command.name} 发生异常: {str(e)}")
            return False
