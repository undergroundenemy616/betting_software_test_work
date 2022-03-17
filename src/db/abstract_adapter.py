from abc import abstractmethod


class AbstractDBAdapter:
    @abstractmethod
    async def get_objects_from_db(self, *args, **kwargs):
        pass

    @abstractmethod
    async def get_object_from_db(self, *args, **kwargs):
        pass

    @abstractmethod
    async def add_object_to_db(self, *args, **kwargs):
        pass

    @abstractmethod
    async def delete_object_from_db(self, *args, **kwargs):
        pass

    @abstractmethod
    async def update_object_from_db(self, *args, **kwargs):
        pass
