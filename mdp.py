import mapFile
from possibleFields import FieldType

mapFileLocation = input("Podaj nazwę pliku z mapą: ")  # np MDP_mapa.txt
readMap = mapFile.MapFile(mapFileLocation, 0.5)  # wczytaj mapę, oblicz T
res = readMap.getOptimalActions(1000)  # znajdź optymalną ścieżkę
potLin = ""  # do wypisania potencjałów
actLin = ""  # do wypisania akcji
for fieldLine in res:  # dla każdej z linii
    for field in fieldLine:  # dla każdego pola
        if field.canEnterThisField is False:  # jeżeli przeszkoda
            potLin += "0\t\t"
            actLin += "0\t"
        elif field.fieldType == FieldType.End:  # jeżeli pole końcowe
            potLin += "{:.2f}".format(field.potential) + "\t"
            actLin += "0\t"
        else:  # jeżeli zwykłe pole
            potLin += "{:.2f}".format(field.potential) + "\t"
            actLin += field.bestAction[1].actionType.name[0] + "\t"
    potLin += "\n"
    actLin += "\n"
print("Mapa potencjałów:")  # wypisz mapy
print(potLin)
print("Polityka ruchu:")
print(actLin)
