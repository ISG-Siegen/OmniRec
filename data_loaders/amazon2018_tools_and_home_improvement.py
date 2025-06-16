from .amazon import Amazon


class Amazon2018ToolsAndHomeImprovement(Amazon):

    @staticmethod
    def load_from_file(source_path, user_column_name, item_column_name, rating_column_name, timestamp_column_name,
                       **additional_parameters):
        return super(Amazon2018ToolsAndHomeImprovement,
                     Amazon2018ToolsAndHomeImprovement).load_from_file(source_path, user_column_name, item_column_name,
                                                                       rating_column_name, timestamp_column_name)
