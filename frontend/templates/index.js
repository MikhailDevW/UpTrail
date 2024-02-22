// Создание карты
var myMap = new ymaps.Map('map', {
    center: [55.755814, 37.617635],
    zoom: 10
});

// Получение границ видимой области карты
var bounds = myMap.getBounds();

// Вывод координат границ видимой области
console.log('Верхняя левая точка: ' + bounds[0]);
console.log('Нижняя правая точка: ' + bounds[1]);