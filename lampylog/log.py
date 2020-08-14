import logging
from pythonjsonlogger import jsonlogger
from datetime import datetime
from typing import Dict


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Set up the custom formatter, passing konsentus specific log names."""

    def add_fields(self, log_record: Dict, record, message_dict):
        """Add custom log fields to formatter"""
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get("timestamp"):
            # this doesn't use record.created, so it is slightly off
            (dt, micro) = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f").split(".")
            now = "%s.%03d" % (dt, int(micro) / 1000)
            log_record["timestamp"] = now

        if log_record.get("level"):
            log_record["level"] = log_record["level"].lower() + "x"
        else:
            if record.levelname.lower() == "warning":
                record.levelname = "warn"
            log_record["level"] = record.levelname.lower()


def compose(logger):
    """Correctly maps python log level to the konsentus log levels."""

    def curriedLogger(level, content):
        if level == "error":
            return logger.error(content)
        if level == "warn":
            return logger.warn(content)
        if level == "info":
            return logger.info(content)
        if level == "metric":
            return logger.metric(content)
        if level == "verbose":
            return logger.verbose(content)
        if level == "debug":
            return logger.debug(content)

    return curriedLogger


def get_logger(logger_name, log_level):
    """Configure and return default logger."""

    logger = logging.getLogger(logger_name)

    logger.setLevel(log_level)

    logger.warn = logger.warning
    logger.metric = logger.info  # Need to treat this as a metric, not an info
    logger.verbose = logger.info
    logger.log = compose(logger)

    formatter = CustomJsonFormatter(
        "(timestamp) (level) (message) (aws_request_id) (invoked_function_arn)"
    )

    for handler in logging.root.handlers:
        handler.setFormatter(formatter)

    return logger
