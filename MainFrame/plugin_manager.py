import os
import sys
import importlib
import importlib.util

class PluginManager:
    """ 插件管理 """

    def __init__(self, path='Plugin', file_name_ends='service.py'):
        """ 调用时将插件注册 """
        if not os.path.isdir(path):
            raise EnvironmentError('%s 不是文件夹！' % path )
        self.all_plugins = {}
        self.register_all_plugin(path, file_name_ends)

    def register_all_plugin(self, path, file_name_ends):
        """ 递归检测插件路径下的所有插件，注册插件 """
        plugin_path = path
        items = os.listdir(plugin_path)
        for item in items:
            if os.path.isdir(os.path.join(plugin_path, item)) and item != '__pycache__':
                p_path = os.path.join(plugin_path, item)
                self.register_all_plugin(p_path, file_name_ends)
            else:
                if item.endswith(file_name_ends) and item != '__init__.py':
                    module_name = item[:-3]
                    if module_name not in sys.modules:
                        module_name = '.'.join([plugin_path, module_name]).replace('\\', '.')
                        module_spec = importlib.util.find_spec(module_name)
                        if module_spec:
                            module = importlib.util.module_from_spec(module_spec)
                            module_spec.loader.exec_module(module)
                            self.all_plugins[module_name] = module
                            print('加载插件：', module_name)

    def unregister_plugin(self, plugin_name):
        """ 注销插件 """
        if plugin_name in self.all_plugins:
            del self.all_plugins[plugin_name]

    def get_plugin_by_name(self, plugin_name):
        """ 按名称获取插件，用于插件之间的交互 """
        plugin = self.all_plugins[plugin_name] if plugin_name in self.all_plugins else None
        return plugin

    def get_all_plugin(self):
        """ 获取所有插件 """
        return self.all_plugins
