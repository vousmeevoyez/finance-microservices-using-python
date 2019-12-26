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
    create_afpi_report_entry,
    generate_afpi_report,
    upload_file_via_ftp,
    ReportServicesError
)


@api.route("/afpi/download/<string:regulation_report_id>")
class AfpiDownloadRoutes(Resource):
    """
        download file from afpi
    """
    def get(self, regulation_report_id=None):
        try:
            zip_name = generate_afpi_report(regulation_report_id)
        except ReportServicesError:
            return {"status": "DOWNLOAD_FAILED"}, 422
        else:
            return send_file(
                "../../{}".format(zip_name),
                as_attachment=True,
                cache_timeout=0
            )


@api.route("/afpi/upload")
class AfpiUploadRoutes(Resource):
    """
        for manual upload to afpi server
    """
    def post(self):
        file_ = request.files['file']

        if file_ and allowed_file(file_.filename):
            try:
                upload_file_via_ftp(io.BytesIO(file_.read()), file_.filename)
            except ReportServicesError:
                return {"status": "UPLOAD_FAILED"}, 422
            else:
                return {"status": "UPLOAD_COMPLETED"}


@api.route("/afpi/create")
class AfpiGenerateRoutes(Resource):
    """ create regulation report entry and extract all loan + borrower info """
    def post(self):
        try:
            regulation_report = create_afpi_report_entry()
        except ReportServicesError:
            return {"status": "CREATE_FAILED"}, 422
        return {"id": str(regulation_report.id)}
