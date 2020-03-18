"""
    Routes
    ___________
    this is where our flask app define all url
"""
import io
from flask_restplus import Resource
from flask import send_file, request

from app.api.report import api
from app.api.lib.core.routes import Routes
from app.api.lib.utils import allowed_file

from app.api.report.modules.services import (
    IdReportServices,
    DateTimeReportServices,
    ReportServicesError,
)


@api.route("/afpi/download/<string:regulation_report_id>")
class AfpiDownloadRoutes(Resource):
    """
        download file from afpi
    """

    def get(self, regulation_report_id):
        try:
            zip_name = IdReportServices(
                regulation_report_id
            ).generate_afpi_report()
        except ReportServicesError:
            return {"status": "DOWNLOAD_FAILED"}, 422
        else:
            return send_file(
                "../../{}".format(zip_name),
                as_attachment=True,
                cache_timeout=0
            )


@api.route("/afpi/upload/<string:regulation_report_id>")
class AfpiUploadRoutes(Resource):
    """
        for manual upload to afpi server
    """

    def post(self, regulation_report_id):
        file_ = request.files["file"]

        if file_ and allowed_file(file_.filename):
            try:
                IdReportServices(
                    regulation_report_id
                ).upload_file_via_ftp(
                    io.BytesIO(file_.read()), file_.filename
                )
            except ReportServicesError:
                return {"status": "UPLOAD_FAILED"}, 422
            else:
                return {"status": "UPLOAD_COMPLETED"}


@api.route("/afpi/create")
class AfpiGenerateRoutes(Resource):
    """ create regulation report entry and extract all loan + borrower info """

    def post(self):
        try:
            loans, regulation_report_id = DateTimeReportServices(
                is_today=True
            ).create_or_update_loans()
        except ReportServicesError:
            return {"status": "CREATE_FAILED"}, 422
        return {"id": regulation_report_id}
