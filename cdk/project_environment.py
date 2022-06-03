import yaml

class ProjectEnvironment():
    @property
    def configurations(self):
        return self._configurations

    def __init__(self, env='default') -> None:
        self.env = env        
        self.loadConfig()
        pass

    def loadConfig(self):
        env = self.env
        with open(f'config/{env}.yml', 'r') as stream:
            try:
                self._configurations = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                raise yaml.YAMLError(exc)
        

if __name__ == '__main__':
    print ("class ProjectEnvironment")
    #main()