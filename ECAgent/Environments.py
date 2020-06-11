from ECAgent.Core import Agent, Environment, Component, Model


class PositionComponent(Component):
    """ A position component. It contains three float properties: x, y, z.
    This component can be used to store the position of an Agent in a 1-3D world.
    It is used by the LineWorld, GridWorld and CubeWorld classes to do exactly that."""

    def __init__(self, agent, model, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None:
        super().__init__(agent, model)
        self.x = x
        self.y = y
        self.z = z


class LineWorld(Environment):
    """ LineWorld is a discrete environment with only 1 axis (x-axis). It can be used in place of the base Environment
    class. All agents added to a LineWorld class are given a PositionComponent to denote their place in the world.

    A LineWorld's dimensions are defined by a width property.

    LineWorld.addCellComponent(comp) adds component comp to each of the cells in the environment."""

    def __init__(self, width, model, id: str = 'ENVIRONMENT'):

        if width < 1:
            raise Exception("Cannot create a LineWorld with a negative width.")

        super().__init__(model, id=id)
        self.width = width
        self.cells = []

        # Create cells
        for x in range(width):
            self.cells.append(Agent('CELL_' + str(x), self.model))
            self.cells[x].addComponent(PositionComponent(self.cells[x], self.model, x=x))

    def addAgent(self, agent: Agent, xPos: int = 0):
        """Adds an agent to the environment. Overrides the base class function.
        This function will also add a PositionComponent to the agent object.
        If the xPos is greater than the width of the world, an error will be thrown."""

        if xPos >= self.width or xPos < 0:
            raise Exception("Cannot add the Agent to position not on the map.")

        agent.addComponent(PositionComponent(agent, agent.model, x=xPos))
        super().addAgent(agent)

    def addCellComponent(self, generator):
        """ Adds the component supplied by the generator functor to each of the cells.
        The functor is supplied with the cell as input"""
        for cell in self.cells:
            generator(cell)

    def removeAgent(self, agentID: str):
        """ Removes the agent from the environment. Will also remove the PositionComponent from the agent"""
        if agentID in self.agents:
            self.agents[agentID].removeComponent(PositionComponent)

        super().removeAgent(agentID)

    def setModel(self, model: Model):
        super().setModel(model)

        for cell in self.cells:
            xPos = cell[PositionComponent].x
            cell.removeComponent(PositionComponent)
            cell.model = model
            cell.addComponent(PositionComponent(cell, self.model, x=xPos))

    def getAgentsAt(self, xPos: int):
        """Returns a list of agents at position xPos. Will return [] empty if no agents are in that cell"""
        return [self.agents[agentKey] for agentKey in self.agents if self.agents[agentKey][PositionComponent].x == xPos]

    def getDimensions(self):
        return self.width

    def getCell(self, x: int):
        if x < 0 or x >= len(self.cells):
            return None
        else:
            return self.cells[x]


class GridWorld(Environment):
    """ GridWorld is a discrete environment with 2 axes (x,y-axes). It can be used in place of the base Environment
    class. All agents added to a GridWorld class are given a PositionComponent to denote their place in the world.

    A GridWorld's dimensions are defined by a width and height properties.

    GridWorld.addCellComponent(comp) adds component comp to each of the cells in the environment."""

    def __init__(self, width, height, model, id: str = 'ENVIRONMENT'):

        if width < 1 or height < 1:
            raise Exception("Cannot create a GridWorld with a negative width or height.")

        super().__init__(model, id=id)
        self.width = width
        self.height = height
        self.cells = []

        # Create cells
        for y in range(height):
            for x in range(width):
                agentID = x + (y * self.width)
                self.cells.append(Agent('CELL_' + str(agentID), self.model))
                self.cells[agentID].addComponent(PositionComponent(self.cells[agentID], self.model, x=x, y=y))

    def addAgent(self, agent: Agent, xPos: int = 0, yPos: int = 0):
        """Adds an agent to the environment. Overrides the base class function.
        This function will also add a PositionComponent to the agent object.
        If the xPos or yPos is greater than the width of the world, an error will be thrown."""

        if xPos >= self.width or xPos < 0 or yPos >= self.height or yPos < 0:
            raise Exception("Cannot add the Agent to position not on the map.")

        agent.addComponent(PositionComponent(agent, agent.model, x=xPos, y=yPos))
        super().addAgent(agent)

    def addCellComponent(self, generator):
        """ Adds the component supplied by the generator functor to each of the cells.
        The functor is supplied with the cell as input"""
        for cell in self.cells:
            generator(cell)

    def removeAgent(self, agentID: str):
        """ Removes the agent from the environment. Will also remove the PositionComponent from the agent"""
        if agentID in self.agents:
            self.agents[agentID].removeComponent(PositionComponent)

        super().removeAgent(agentID)

    def setModel(self, model: Model):
        super().setModel(model)

        for cell in self.cells:
            x, y = cell[PositionComponent].x, cell[PositionComponent].y
            cell.removeComponent(PositionComponent)
            cell.model = model
            cell.addComponent(PositionComponent(cell, self.model, x=x, y=y))

    def getAgentsAt(self, xPos: int, yPos: int):
        """Returns a list of agents at position xPos. Will return [] empty if no agents are in that cell"""
        return [self.agents[agentKey] for agentKey in self.agents
                if self.agents[agentKey][PositionComponent].x == xPos and self.agents[agentKey][PositionComponent].y == yPos]

    def getDimensions(self):
        return self.width, self.height

    def getCell(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return None
        else:
            return self.cells[x + (y * self.width)]


class CubeWorld(Environment):
    """ CubeWorld is a discrete environment with 3 axes (x,y,z-axes). It can be used in place of the base Environment
    class. All agents added to a GridWorld class are given a PositionComponent to denote their place in the world.

    A CubeWorld's dimensions are defined by a width, height and depth properties.

    CubeWorld.addCellComponent(comp) adds component comp to each of the cells in the environment."""

    def __init__(self, width, height, depth, model, id: str = 'ENVIRONMENT'):

        if width < 1 or height < 1 or depth < 1:
            raise Exception("Cannot create a CubeWorld with a negative width or height.")

        super().__init__(model, id=id)
        self.width = width
        self.height = height
        self.depth = depth
        self.cells = []

        # Create cells
        for z in range(depth):
            for y in range(height):
                for x in range(width):
                    agentID = (z * self.width * self.height) + (y * width) + x
                    self.cells.append(Agent('CELL_' + str(agentID), self.model))
                    self.cells[agentID].addComponent(PositionComponent(self.cells[agentID], model, x, y, z))

    def addAgent(self, agent: Agent, xPos: int = 0, yPos: int = 0, zPos: int = 0.0):
        """Adds an agent to the environment. Overrides the base class function.
        This function will also add a PositionComponent to the agent object.
        If the xPos, yPos or zPos is greater than the width of the world, an error will be thrown."""

        if xPos >= self.width or xPos < 0 or yPos >= self.height or yPos < 0 or zPos >= self.depth or zPos < 0:
            raise Exception("Cannot add the Agent to position not on the map.")

        agent.addComponent(PositionComponent(agent, agent.model, x=xPos, y=yPos, z=zPos))
        super().addAgent(agent)

    def addCellComponent(self, generator):
        """ Adds the component supplied by the generator functor to each of the cells.
        The functor is supplied with the cell as input"""
        for cell in self.cells:
            generator(cell)

    def removeAgent(self, agentID: str):
        """ Removes the agent from the environment. Will also remove the PositionComponent from the agent"""
        if agentID in self.agents:
            self.agents[agentID].removeComponent(PositionComponent)

        super().removeAgent(agentID)

    def setModel(self, model: Model):
        super().setModel(model)

        for cell in self.cells:
            xPos = cell[PositionComponent].x
            yPos = cell[PositionComponent].y
            zPos = cell[PositionComponent].z
            cell.removeComponent(PositionComponent)
            cell.model = model
            cell.addComponent(PositionComponent(cell, self.model, xPos, yPos, zPos))

    def getAgentsAt(self, xPos: int, yPos: int, zPos: int):
        """Returns a list of agents at position xPos. Will return [] empty if no agents are in that cell"""
        return [self.agents[agentKey] for agentKey in self.agents
                if self.agents[agentKey][PositionComponent].x == xPos and self.agents[agentKey][PositionComponent].y == yPos and self.agents[agentKey][PositionComponent].z == zPos]

    def getDimensions(self):
        return self.width, self.height, self.depth

    def getCell(self, x, y, z):
        if x < 0 or x >= self.width or y < 0 or y >= self.height or z < 0 or z >= self.depth:
            return None
        else:
            return self.cells[x + self.width * (y + self.depth * z)]
