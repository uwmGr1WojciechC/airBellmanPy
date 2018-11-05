import possibleFields


class MapField:
    def __init__(self, fieldType, fieldCost, x, y):
        self.fieldType = fieldType
        self.fieldCost = fieldCost
        self.canEnterThisField = True if self.fieldType != possibleFields.FieldType.Obstacle else False  # jeżeli to przeszkoda to nie wchodź
        self.x = x  # koordynaty
        self.y = y
        self.actionsList = []
        self.bestAction = None
        self.potential = fieldCost
        self.potentialCalculated = False  # true jeżeli moduł z nowej wart. i starej < 10^-4
