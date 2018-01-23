# coding: utf-8
import csv

from ideApp.CodePersistenceBackends.MongoDB.mongodb_models import RepositoryModel

with open('repository_model_201801231212.csv', 'r') as csv_fd:
    csv_reader = csv.reader(csv_fd, delimiter=',', quotechar='"')
    first_row = False
    for row in csv_reader:
        if type(first_row) == bool:
            first_row = row
        else:
            vals_dict = {}
            for header_index in range(len(first_row)):
                if header_index < len(row):
                    if first_row[header_index] != '_cls':
                        if first_row[header_index] == '_id':
                            first_row[header_index] = 'pk'
                        vals_dict[first_row[header_index]] = row[header_index]
            print(vals_dict)
            repository = RepositoryModel(**vals_dict)
            print(repository)
            repository.save()
            print(repository)
