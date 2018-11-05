from possibleActions import ActionType


class Action:
    def __init__(self, startState, endState, actionType):
        self.startState = startState
        self.endState = endState
        self.actionType = actionType
        self.assocActions = self.getActionBind(self.actionType)
        self.mainActionProb = 0.8
        self.assocActionProb = 0.1
        self.mainTvalue = None
        self.assocTvalues = None
        self.noStateChangeProb = 0
        self.noAltStateChangeProb = 0

    def getActionBind(self, actType):  # zwraca akcje powiązane z wybraną
        if actType == ActionType.Up:
            return ActionType.Right, ActionType.Left
        elif actType == ActionType.Right:
            return ActionType.Up, ActionType.Down
        elif actType == ActionType.Down:
            return ActionType.Right, ActionType.Left
        elif actType == ActionType.Left:
            return ActionType.Up, ActionType.Down
