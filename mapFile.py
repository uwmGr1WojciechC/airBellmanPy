from operator import itemgetter
from possibleActions import ActionType
from possibleFields import FieldType
import mapField
import action


class MapFile:
    def __init__(self, mapLocation, gamma):
        with open(mapLocation) as mp:
            self.mapFile = mp.readlines()
        self.mapWidth = int(self.mapFile[0].split()[0])  # wczytaj wymiary macierzy
        self.mapHeight = int(self.mapFile[0].split()[1])

        del self.mapFile[0]  # usuń wczytane wymiary macierzy
        self.gamma = gamma
        self.mapFields = []  # przygotuj miejsce na wczytanie pól mapy

        # wczytanie pól mapy
        for line in range(0, self.mapHeight):
            mapLine = self.mapFile[line].split()  # przygotuj typy każdego z pól
            fieldCost = self.mapFile[
                self.mapHeight + 1 + line].split()  # przygotuj koszt każdego z pól (przejdź z przesunięciem)
            mapFiledsLine = []  # miejsce na tymczasową tablicę z aktualną linią
            for field in range(0, len(mapLine)):  # dla każdego z pól w linii mapy, dodaj je do listy
                mapFiledsLine.append(
                    mapField.MapField(FieldType(int(mapLine[field])), float(fieldCost[field]), field, line))
            self.mapFields.append(mapFiledsLine)  # dodaj linię z polami do mapy

        # wyznaczenie T dla pól mapy
        for fieldLine in self.mapFields:  # dla każdej z linii
            for field in fieldLine:  # dla każdego pola
                if field.canEnterThisField is False or field.fieldType == FieldType.End:  # poza przeszkodami i polami końcowymi
                    continue
                for act in ActionType:  # dla każdej akcji
                    stateTrans = action.Action(field, self.getNextState(field, act), act)  # przygotuj obiekt dla aktualnej akcji
                    if stateTrans.endState is None:  # jeżeli trafiamy na przeszkodę lub koniec mapy
                        stateTrans.noStateChangeProb = stateTrans.mainActionProb
                    else:
                        stateTrans.mainTvalue = stateTrans.mainActionProb  # jeżeli można się ruszyć to przypisz wartość
                    altAct = []  # prawdopodobieństwa i rodzaje alternatywnych wyborów
                    for a in stateTrans.assocActions:  # dla każdej z alternatywnych akcji sprawdź czy można je zrobić
                        alternateAct = self.getNextState(field, a)
                        if alternateAct is None:  # jeżeli trafimy np. na przeszkodę lub brzeg mapy w alternatywnym kierunku
                            stateTrans.noStateChangeProb += stateTrans.assocActionProb
                            stateTrans.noAltStateChangeProb += stateTrans.assocActionProb  # ustal prawdop. zostania na miejscu
                            altAct.append((None, a, None))  # dodaj do listy prawdopodobieństwo przejścia do innego stanu i ten stan oraz akcja
                        else:  # jeżeli możemy przejść w alternatywnym kierunku
                            altAct.append((stateTrans.assocActionProb, a, alternateAct))
                    stateTrans.assocTvalues = altAct
                    field.actionsList.append(stateTrans)  # i dodaj go do listy

    def getStateWithCoordinates(self, y, x):
        if 0 <= x < self.mapWidth and 0 <= y < self.mapHeight:  # jeżeli pole istnieje
            if self.mapFields[y][x].canEnterThisField is False:  # jeżeli jest przeszkodą to nie można wejść więc None
                return None
            return self.mapFields[y][x]  # jeżeli można wejść to zwróć pole
        else:  # jeżeli pole jest poza mapą to None
            return None

    def getNextStateCoordinates(self, currentState, currentAction):
        act = int(currentAction.value[2])
        if act == 0:  # jeżeli przesuwamy się w lewo lub prawo
            return currentState.y, currentState.x + int(currentAction.value[:2])
        elif act == 1:  # jeżeli przesuwamy się w górę lub dół
            return currentState.y + int(currentAction.value[:2]), currentState.x

    def getNextState(self, currentState, currentAction):
        ycoord, xcoord = self.getNextStateCoordinates(currentState, currentAction)
        return self.getStateWithCoordinates(ycoord, xcoord)  # znajdź stan dla podanych koordynatów

    def getOptimalActions(self, cycles):
        for i in range(0, cycles):
            for fieldLine in self.mapFields:  # dla każdej z linii
                for field in fieldLine:  # dla każdego pola
                    if field.canEnterThisField is False or field.fieldType == FieldType.End:  # poza przeszkodami i polami końcowymi
                        continue
                    if field.potentialCalculated is True:  # jeżeli poprzednia różnica między nową i starą wartością potencjału była < 10^-4 to pomiń
                        continue

                    tmpsum = []  # miejsce na wyniki dla danej akcji
                    actSum = []  # miejsce na sumy dla każdej z akcji dla danego pola
                    for a in field.actionsList:  # dla każdej z akcji stanu s
                        if a.endState is not None:  # jeżeli można przejść dalej
                            tmpsum.append(a.mainTvalue * a.endState.potential)
                        else:  # jeżeli nie można, to wynikiem jest zostanie na danym polu
                            tmpsum.append(a.noStateChangeProb * a.startState.potential)
                        for altA in a.assocTvalues:  # dla każdej z alternatywnych akcji (prawdop., akcja, stan końcowy) wobec akcji głównej
                            if altA[2] is not None:  # jeżeli można przejść do alternatywnego stanu
                                tmpsum.append(altA[0] * altA[2].potential)
                            elif altA[2] is None and a.noAltStateChangeProb == a.assocActionProb:  # jeżeli nie można przejść ale taki stan jest tylko 1
                                tmpsum.append(a.noAltStateChangeProb * a.startState.potential)
                            elif altA[2] is None and a.noAltStateChangeProb > a.assocActionProb:  # jeżeli nie można przejść i takich stanów jest więcej niż 1
                                tmpsum.append(a.noAltStateChangeProb * a.startState.potential)
                                break
                        actSum.append((sum(tmpsum), a, a.endState))
                        tmpsum = []
                    field.bestAction = max(actSum, key=itemgetter(0))  # znajdź najlepszą akcję dla stanu s
                    Unew = field.fieldCost + self.gamma * field.bestAction[0]  # oblicz potencjał
                    if abs(field.potential - Unew) < 10E-4:  # jeżeli różnica między nową i starą wart. potencjału jest wystarczająco mała to oznacz że znaleziono wartość
                        field.potentialCalculated = True
                    else:
                        field.potential = Unew
        return self.mapFields
