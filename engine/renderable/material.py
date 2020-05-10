import glm

class Material:
    def __init__(self, materialData):
        self.ambient = glm.vec3(materialData[2]['value'][0], materialData[2]['value'][1], materialData[2]['value'][2])
        self.diffuse = glm.vec3(materialData[3]['value'][0], materialData[3]['value'][1], materialData[3]['value'][2])
        self.specular = glm.vec3(materialData[4]['value'][0], materialData[4]['value'][1], materialData[4]['value'][2])
        self.shininess = materialData[5]['value']

    def draw(self, program):
        program.setVec3('material.ambient', self.ambient)
        program.setVec3('material.diffuse', self.diffuse)
        program.setVec3('material.specular', self.specular)
        program.setFloat('material.shininess', self.shininess)