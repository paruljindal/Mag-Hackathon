import shutil

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from app.core.phase2.class_converter import ClassConverter
from .core.constants import Constants
import json
from app.core.phase2.construct_model import ConstructModel
from app.core.phase3.construct_model import ConstructModel as phase3_construct_model
from app.core.phase3.query_converter import QueryConverter

from app.core.json_handler import JsonHandler
from app.core.phase2.db_converter import DBConverter

from shutil import make_archive
from wsgiref.util import FileWrapper


def generate_classes(request):
    class_converter = ClassConverter()

    # with open(Constants.CONTENT_PHASE2 + 'association.json') as f:
    # with open(Constants.CONTENT_PHASE2 + 'aggregation.json') as f:
    # with open(Constants.CONTENT_PHASE2 + 'composition.json') as f:

    with open(Constants.CONTENT_PHASE2 + 'inheritance.json') as f:
        data = json.load(f)
        Objects = data[str(Constants.INNER_OBJECT)]
        object_model = ConstructModel().construct(Objects)
        class_converter.generate_classes(object_model)

    return HttpResponse("Thanks")


def _delete_files(folder):
    import os
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def _get_classes(request, json_string):
    with open("app/Generated1/" + "temp.json", "w") as temp:
        temp.write(json_string)

    with open("app/Generated1/" + "temp.json", "r") as object_loaded:
        data = json.load(object_loaded)
        files_path = Constants.GENERATED
        class_converter = ClassConverter()
        Objects = data[str(Constants.INNER_OBJECT)]
        object_model = ConstructModel().construct(Objects)
        class_converter.generate_classes(object_model)
        path_to_zip = make_archive(files_path, "zip", files_path)
        response = HttpResponse(FileWrapper(open(path_to_zip, 'rb')), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="Temp.zip"'
        _delete_files("app/Generated1/")
        _delete_files("app/Generated/")
    return response


@csrf_exempt
def get_classes(request):
    if request.method == "POST":
        return _get_classes(request, request.body.decode('utf-8'))


def generate_db_create(request):
    db_converter = DBConverter()
    # with open(Constants.CONTENT_PHASE2 + 'oneToOne.json') as f:
    # with open(Constants.CONTENT_PHASE2 + 'oneToMany.json') as f:

    with open(Constants.CONTENT_PHASE2 + 'manyToMany.json') as f:
        data = json.load(f)
        Objects = data[str(Constants.INNER_OBJECT)]
        object_model = ConstructModel().construct(Objects)
        query_holders = db_converter.db_converter(object_model)
        create_queries = ""
        alter_queries = ""
        for query_holder in query_holders:
            create_queries += query_holder.get_query()
            create_queries += "\n"
            alter_queries += query_holder.get_alter_commands()
            alter_queries += "\n"

    file_object = open(Constants.GENERATED + "GeneratedSql" + ".sql", "w")
    file_object.write(create_queries)
    file_object.write(alter_queries)
    return HttpResponse(create_queries + "\n" + alter_queries + "\n")


def generate_query(request):
    query_converter = QueryConverter()
    with open(Constants.CONTENT_PHASE3 + 'selectQuery1.json') as f:
        data = json.load(f)
        # phase3_query_model Structure will hold the views joins and conditions
        phase3_query_model = phase3_construct_model().construct(
            data["views"],
            data["joins"],
            data["conditions"])

        query_holder = query_converter.generate_query(phase3_query_model)

    return HttpResponse(query_holder)

def generate_query1(request):
    query_converter = QueryConverter()
    with open(Constants.CONTENT_PHASE3 + 'simpleQuery2.json') as f:
        data = json.load(f)
        # phase3_query_model Structure will hold the views joins and conditions
        phase3_query_model = phase3_construct_model().construct(
            data["views"],
            data["joins"],
            data["conditions"])

        query_holder = query_converter.generate_query(phase3_query_model)

    return HttpResponse(query_holder)

def get_json(request):
    json_obj = JsonHandler()
    return_data = json_obj.get_json()
    return HttpResponse(return_data)


def parse_json(request):
    json_obj = JsonHandler()
    return HttpResponse(json_obj.parse_json())


def get_association_mapping(request):
    path = "app/Content/association_mapping.json"
    with open(path, "r") as json_association_mapping:
        mapping_obj = json.load(json_association_mapping)
    return HttpResponse(str(mapping_obj))


def save_json(request):
    if request.method == "POST":
        model_filename = request.session["filename"]
        model_data = request.session["model_data"]
        # json_obj.save_json(model_filename, model_data)
        return HttpResponse("File successfully saved!")
    return HttpResponse("No data received!")


def get_fallback():
    JsonHandler.get_fallback()
    return HttpResponse("Model file restored")


def model_validator(request):
    if request.method == "POST":
        model_filename = request.session["filename"]
        return HttpResponse(JsonHandler.model_validator(model_filename))
    return HttpResponse("No file to Validate!")


def _get_sql_queries(json_object):
    db_converter = DBConverter()
    json_object = json.loads(json_object)
    with open(Constants.GENERATED + "temp.json", "w") as temp:
        temp.write(json_object)

    with open(Constants.GENERATED + "temp.json", "r") as object_loaded:
        json_object = json.load(object_loaded)
        Objects = json_object[Constants.INNER_OBJECT]
        object_model = ConstructModel().construct(Objects)
        query_holders = db_converter.db_converter(object_model)
        create_queries = ""
        alter_queries = ""
        for query_holder in query_holders:
            create_queries += query_holder.get_query()
            create_queries += "\n"
            alter_queries += query_holder.get_alter_commands()
            alter_queries += "\n"
        response_string = create_queries + "\n" + alter_queries
    return response_string


@csrf_exempt
def get_sql(request):
    get_classes_zip = ""
    if request.method == "POST":
        json_string = request.body.decode('utf-8')
        get_classes_zip = _get_sql_queries(json_string)
    _delete_files("app/Generated1/")
    _delete_files("app/Generated/")
    return HttpResponse(str(get_classes_zip))
