from datetime import datetime

from rest_framework import serializers



class ApiResponse:
    status_code: int
    data: object
    error: None
    timestamp: datetime

    def __init__(self, data=None, error=None, status_code=None, timestamp=None):
        self.data = data
        self.error = error
        self.status_code = status_code
        self.timestamp = timestamp if timestamp is not None else datetime.now()


class ApiError(serializers.Serializer):
    error_trace_id = serializers.IntegerField()
    user_message = serializers.CharField()
    developer_message = serializers.CharField()

class ApiResponseSerializer(serializers.Serializer):
    status_code = serializers.IntegerField()
    data = None
    error = ApiError()
    timestamp = serializers.DateTimeField()

    def __init__(self, data_serialize=None, **kwargs):
        super().__init__(**kwargs)
        self.data = data_serialize
