from .rest_channel_factory import MyRestChannelFactory
from .rest_health_check import HealthCheckInput


class MyRestChannelHUL(MyRestChannelFactory):
  channel_name = "hul"


class MyRestChannelHMD(MyRestChannelFactory):
  channel_name = "hmd"
