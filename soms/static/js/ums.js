//THIS FILE IS AUTO-GENERATED
function addNode(x, y, node_layer, nodes, radius, color, text, numberImg) {
	node = {}
	node_layer.activate();
	if (typeof(numberImg) === "undefined") {
		new_node = new paper.Path.Circle(new Point(x, y), radius);
		node['img'] = img[undefined];
	} else {
		new_node = new paper.Raster(img[numberImg], new Point(x, y));
		new_node.on('load', function() {
			new_node.size = new Size(radius * 2, radius * 2);
		});
		node['img'] = img[numberImg];
	}
	new_node.fillColor = color;
	node['x'] = x;
	node['y'] = y;
	node['radius'] = radius;
	node['text'] = text;
	node['type'] = 'node';
	node['color'] = color;
	var text = new PointText();
	text.content = node['text'];
	text.position = new Point(x, y + (radius) + 6);
	new_node.text = text;
	text.fillColor = color;
	text.fontFamily = 'Courier New';
	text.fontWeight = 'bold';
	nodes["Path @" + new_node.id] = node;
	view.draw();
}

function addTrack(x1, y1, x2, y2, color, tracks, track_layer) {
	track = {};
	track_layer.activate();
	xy = new Point(x1, y1);
	x1y1 = new Point(x2, y2);
	new_track = new Path.Line(xy, x1y1);
	new_track.strokeColor = color;
	track['x1'] = x1;
	track['y1'] = y1;
	track['x2'] = x2;
	track['y2'] = y2;
	track['color'] = color;
	tracks[new_track.id] = track;
	view.draw();
}
function SeeNodes(nodes) {
	s = '';
	for (var i in nodes)
		s += "Номер узла: " + i + " Координата х: " + nodes[i]['x'] + " Координата y: " + nodes[i]['y'] + "\n";
	console.log(s);
}

function SeeTracks(tracks) {
	s = '';
	for (var i in tracks) {
		s += "Номер связи: " + i + " Координата х1: " + tracks[i]['x1'] + " Координата y1: " + tracks[i]['y1'] + " Координата х2: " + tracks[i]['x2'] + " Координата y2: " + tracks[i]['y2'] + "\n";
	}
	console.log(s);
}
var qee = [];
var background = {
		drawImg: function(x, y, url, background_layer) {
			background_layer.activate();
			var centerIMG = new Raster({
				source: url,
				position: new Point(x, y)
			});
			view.draw();
		},
		imgUpload: function() { //функция загрузки изображения на страницу
			qee = [];
			var oFile = $('#image_file')[0].files[0];
			$('.error').hide();
			var rFilter = /^(image\/jpeg|image\/png)$/i; //формат жепег и пнг
			if (!rFilter.test(oFile.type)) { //ошибка если неправильный формат
				console.log('Не поддерживаемый формат');;
				return;
			}
			var oReader = new FileReader();
			oReader.onload = function(e) {
				qee.push(e.target.result); //загрузка url изображения в массив
				console.log('Images onload');
			};
			oReader.readAsDataURL(oFile);
		}
	}
	//Переменная для перемещения карты
var drag = false;
//Переменная радиуса узла
var radius = 7;
//Переменная для перемещения узла
var move = false;
//Переменная для установки картинки узла
var img = ['http://get-wallpapers.ru/img/picture/Apr/16/1ff6fb6fbe563ad852a7337c6b306f3b/4.jpg'];
var selected = false;
var drag_start = {};
var drag = false;
var selected2 = false;
var control_selected = false;
var new_node, text, new_track;
paper.install(window);
$(document).ready(function() {
	$('body').on('contextmenu', '#myCanvas', function(e) {
		return false;
	});
	paper.setup("myCanvas");
	paper.view.viewSize.height = $(document).height();
	paper.view.viewSize.width = $(document).width();
	var backgroundURL = '';
	var x1x = 844,
		y1y = 452;
	NowSelected = '';
	NowSelected1 = '';
	NowSelectedTrack = '';
	var background_layer = new Layer();
	$('#img_print').on('click', function(event) { //добавления изображения
		background_layer.clear();
		background.drawImg(x1x, y1y, qee[0], background_layer);
	});

	background_layer.activate();
	var cursor;
	var cursorLayer = new Layer();
	cursorLayer.activate();
	cursor = new Shape.Circle(paper.view.center, radius / 2);
	cursor.fillColor = 'red';
	var track_layer = new Layer();
	var node_layer = new Layer();
	var tool = new Tool();
	var nodes = {};
	var tracks = {};
	var hitOptions = {
		stroke: true,
		fill: true
	};
	tool.onMouseUp = function(event) { //Инструмент для отпускание мышки
		if (event.event.button == 2) { //Для Средней КМ
			drag = false; //Отменить перетаскивание
		}
	};
	function find(array, value) {
		if (array.indexOf) { // если метод существует
			return array.indexOf(value);
		}

		for (var i = 0; i < array.length; i++) {
			if (array[i] === value) return i;
		}

		return -1;
	}
	var dlyamove = [];
	var dlyamove1 = [];
	var dlyamove2 = [];
	var dlyamove3 = [];
	var itemok;
	var seg = [];
	tool.onMouseDrag = function(event) { //Инструмет для перетаскивания элементов
		if (event.event.button == 0) { //Для ЛКМ
			var hitResult = paper.project.hitTest(event.point, hitOptions);
			if (move) { //Если mpve = true, будет выполнена функция переноса узлов (связей)
				MoveToX = event.point.x; //Текущие координаты курсора X
				MoveToY = event.point.y; //Текущие координаты курсора У
				var items = project.getItems({
					class: Path
				});
				var itemsRaster = project.getItems({
					class: Raster
				});
				NowSelected.position['x'] = MoveToX; //Привызка координат курсора Х к выделенному узлу
				NowSelected.position['y'] = MoveToY; //Привязка координат курсора У к выделенному узлу
				NowSelected.text.position['x'] = MoveToX; //Привыязка координат курсора Х  к выделенному узлу (тексту)
				NowSelected.text.position['y'] = MoveToY + 15; //Привязка координат кусора У + 15 к выделенному узлу (тексту)
				for (var i in nodes) {
					if (typeof(nodes[NowSelected]) !== "undefined") {
						nodes[NowSelected]["x"] = MoveToX;
						nodes[NowSelected]["y"] = MoveToY;
					} else { //для картинок
						nodes["Path @" + NowSelected.id]["x"] = MoveToX;
						nodes["Path @" + NowSelected.id]["y"] = MoveToY;
					}

				}
				for (var i = 0, j = 0; i < dlyamove2.length, j < seg.length; i++, j++) { //перемещение линий вместе с узлами
					if (seg[j] == 0) { //если сегмент 0 (начало),, то изменяются координаты начального сегмента
						if (typeof(items.segments) !== "undefined") {
							itemsRaster[dlyamove2[i]].segments[seg[j]].point.x = MoveToX;
							itemsRaster[dlyamove2[i]].segments[seg[j]].point.y = MoveToY;
						} else {
							items[dlyamove2[i]].segments[seg[j]].point.x = MoveToX;
							items[dlyamove2[i]].segments[seg[j]].point.y = MoveToY;
						}
					} else if (seg[j] == 1) { //если сегмент 1 (конец),, то изменяются координаты конечного сегмента
						if (typeof(items.segments) !== "undefined") {
							itemsRaster[dlyamove2[i]].segments[seg[j]].point.x = MoveToX;
							itemsRaster[dlyamove2[i]].segments[seg[j]].point.y = MoveToY;
						} else {
							items[dlyamove2[i]].segments[seg[j]].point.x = MoveToX;
							items[dlyamove2[i]].segments[seg[j]].point.y = MoveToY;
						}

					}
				}

				for (var i in tracks) { //добавление инфы в данные линий, для последующего перемещения
					var data = 0;
					while (data < dlyamove.length) {
						if (seg[data] == 0) {
							tracks[dlyamove[data]]['x1'] = MoveToX;
							tracks[dlyamove[data]]['y1'] = MoveToY;
						} else if (seg[data] == 1) {
							tracks[dlyamove[data]]['x2'] = MoveToX;
							tracks[dlyamove[data]]['y2'] = MoveToY;
						}
						data++;
					}
				}
				paper.view.draw();
			}
		}
		if (event.event.button == 1) { //Для ПКМ
			if (!drag) return; //Если drwa != true то ничего не делать
			var dx = (event.event.pageX - drag_start.x) / paper.view.zoom; // Переменная для перемещения по оси X
			var dy = (event.event.pageY - drag_start.y) / paper.view.zoom; // Переменная для перемещения по оси Y
			paper.view.center = new Point(drag_center.x - dx, drag_center.y - dy); //Перемещение карты по координатам dx/dy
		}
	};
	tool.onMouseDown = function(event) {
		var hitResult = paper.project.hitTest(event.point, hitOptions);
		if (event.event.button == 0) {
			cursor.position = event.point;
			if (hitResult && hitResult.item && hitResult.item != cursor && hitResult.item.className != 'PointText') {
				selected2.selected = false;
				selected2 = false;
				selected2.fillColor = 'red';
				selected2 = hitResult.item;
				hitResult.item.selected = true;
				NowSelected1 = hitResult.item;
				// console.log(NowSelected1.id);
				paper.view.draw();

			}
		}
		if (event.event.button == 2) {
			if (hitResult && hitResult.item && hitResult.item != cursor && hitResult.item.className != 'PointText') {
				paper.project.deselectAll(); //что то делаем
				selected.selected = false;
				move = false;
				dlyamove = [];
				dlyamove1 = [];
				dlyamove2 = [];
				dlyamove3 = [];
				seg = [];
				selected = hitResult.item;
				hitResult.item.selected = true;
				NowSelected = hitResult.item;
				NowSelectedTrack = hitResult.item;
				var items = project.getItems({
					class: Path
				});
				var itemsRaster = project.getItems({
					class: Raster
				});
				for (var i in items) { //получаем все ID узлов и линий на карте
					dlyamove1.push(items[i].id); //добавляем в массив
				}
				for (var i in itemsRaster) { //получаем все ID узлов и линий на карте
					dlyamove1.push(itemsRaster[i].id); //добавляем в массив
				}
				for (var i in tracks) {
					if ((NowSelected.position['x'] == tracks[i]['x1']) && (NowSelected.position['y'] == tracks[i]['y1'])) {
						dlyamove.push(i); //если начальные координаты совпадают, то доавбяется ID линнии в массив + сегмент 0 (начало)
						seg.push(0);
					} else if ((NowSelected.position['x'] == tracks[i]['x2']) && (NowSelected.position['y'] == tracks[i]['y2'])) {
						dlyamove.push(i); //если конечные координаты совпадают, то доавбяется ID линнии в массив + сегмент 1 (конец)
						seg.push(1);
					}
				}
				for (var i = 0; i < dlyamove.length; i++) { //добавление в массив тех линий, которые входят в выделенный узел
					dlyamove2.push((find(dlyamove1, Number(dlyamove[i]))));
				}
				console.log(nodes)
				console.log('id: ' + hitResult.item.id);
				paper.view.draw();

			}
		}
		if (event.event.button == 1) {
			drag = true;
			drag_start.x = event.event.pageX;
			drag_start.y = event.event.pageY;
			drag_center = new Point(paper.view.center);
		}
	};
	//ДОБАВЛЕНИЕ ПУТИ
	$('#draw_track').on('click', function(event) {
		var x1 = 247,
			y1 = 247,
			x2 = 477,
			y2 = 245;
		console.log(NowSelected1.position['x']);
		addTrack(NowSelected.position['x'], NowSelected.position['y'], NowSelected1.position['x'], NowSelected1.position['y'], tracks, track_layer);
	})
	var data = {
		"node": {
			"text": [],
			"color": [],
			"x": [],
			"y": [],
			"img": [],
		},
		"track": {
			"x1": [],
			"y1": [],
			"x2": [],
			"y2": [],
			"color": [],
		}
	};
	var redo = {
		"type": [],
		"node": {
			"text": [],
			"color": [],
			"x": [],
			"y": [],
			"img": [],
		},
		"track": {
			"x1": [],
			"y1": [],
			"x2": [],
			"y2": [],
			"color": [],
		}
	};
	tool.onKeyDown = function(event) {
		if (Key.isDown('r')) {
			move = true;
			redo = {
				"type": [],
				"node": {
					"text": [],
					"color": [],
					"x": [],
					"y": [],
					"img": [],
				},
				"track": {
					"x1": [],
					"y1": [],
					"x2": [],
					"y2": [],
					"color": [],
				}
			};
			paper.view.draw();
		} else if (Key.isDown('f')) {
			data = {
				"node": {
					"text": [],
					"color": [],
					"x": [],
					"y": [],
					"img": [],
				},
				"track": {
					"x1": [],
					"y1": [],
					"x2": [],
					"y2": [],
					"color": [],
				}
			};
			for (var i in nodes) {
				data["node"]["text"].push(nodes[i]["text"]);
				data["node"]["color"].push(nodes[i]["color"]);
				data["node"]["x"].push(nodes[i]["x"]);
				data["node"]["y"].push(nodes[i]["y"]);
				data["node"]["y"].push(nodes[i]["y"]);
				data["node"]["img"].push(nodes[i]["img"]);
			}
			for (var i in tracks) {
				data["track"]["x1"].push(tracks[i]["x1"]);
				data["track"]["y1"].push(tracks[i]["y1"]);
				data["track"]["x2"].push(tracks[i]["x2"]);
				data["track"]["y2"].push(tracks[i]["y2"]);
				data["track"]["color"].push(tracks[i]["color"]);
			}
			var json = JSON.stringify(data);
			var blob = new Blob([json], {
				type: "application/json"
			});
			var url = URL.createObjectURL(blob);

			var a = document.createElement('a');
			a.download = "backup.json";
			a.href = url;
			a.textContent = "Скачать";
			// a;
			document.getElementById('content').appendChild(a);
			// console.log(data);
			view.draw();


		} else if (Key.isDown('q')) {
			var color = document.getElementById('id_color').value;
			var text = document.getElementById('id_text').value;
			if (document.getElementById('type').value == "1") {
				addNode(cursor.position['x'], cursor.position['y'], node_layer, nodes, 10, color, text);
			} else if (document.getElementById('type').value == "2") {
				addNode(cursor.position['x'], cursor.position['y'], node_layer, nodes, 10, color, text, 0);
			}
		} else if (Key.isDown('e')) {
			addTrack(NowSelected.position['x'], NowSelected.position['y'], NowSelected1.position['x'], NowSelected1.position['y'], 'green', tracks, track_layer);

		} else if (Key.isDown('v')) {
			var items = project.getItems({
				class: Path
			});
			console.log(items);

		} else if (Key.isDown('n')) {
			console.log(redo)
		} else if (Key.isDown('g')) {
			var undo = [];

			var items = project.getItems({
				class: Path,
			});

			var itemsRaster = project.getItems({
				class: Raster
			});
			for (var i in items) {
				undo.push(items[i].id)
			}
			for (var i in itemsRaster) {
				undo.push(itemsRaster[i].id)
			}
			undo.sort(compareNumeric);
			for (var i in itemsRaster) {
				if (itemsRaster[i].id === undo[0]) {
					console.log(nodes["Path @" + itemsRaster[i].id])
					redo["node"]["text"].push(nodes["Path @" + itemsRaster[i].id]["text"]);
					redo["node"]["color"].push(nodes["Path @" + itemsRaster[i].id]["color"]);
					redo["node"]["x"].push(nodes["Path @" + itemsRaster[i].id]["x"]);
					redo["node"]["y"].push(nodes["Path @" + itemsRaster[i].id]["y"]);
					redo["node"]["img"].push(nodes["Path @" + itemsRaster[i].id]["img"]);
					redo["type"].push("node");
					itemsRaster[i].text.remove();
					itemsRaster[i].remove();
					console.log("Undo node id: " + itemsRaster[i].id)
				}
			}
			for (var i in items) {
				if (items[i].id === undo[0]) {
					if (typeof(items[i].text) !== "undefined") {
						redo["node"]["text"].push(nodes[items[i]]["text"]);
						redo["node"]["color"].push(nodes[items[i]]["color"]);
						redo["node"]["x"].push(nodes[items[i]]["x"]);
						redo["node"]["y"].push(nodes[items[i]]["y"]);
						redo["node"]["img"].push(nodes[items[i]["img"]])
						redo["type"].push("node");
						items[i].text.remove();
						items[i].remove();
						console.log("Undo node id: " + items[i].id)
					} else {
						redo["track"]["x1"].push(tracks[items[i].id]["x1"]);
						redo["track"]["y1"].push(tracks[items[i].id]["y1"]);
						redo["track"]["x2"].push(tracks[items[i].id]["x2"]);
						redo["track"]["y2"].push(tracks[items[i].id]["y2"]);
						redo["track"]["color"].push(tracks[items[i].id]["color"]);
						redo["type"].push("track");
						items[i].remove();
						console.log("Undo track id: " + items[i].id)
					}
					delete tracks[items[i].id]
				}

			}
			console.log(redo["node"])
			paper.view.draw();
		} else if (Key.isDown('h')) {
			if (redo["type"][0] === "track") {
				addTrack(redo["track"]["x1"][0], redo["track"]["y1"][0], redo["track"]["x2"][0], redo["track"]["y2"][0], redo["track"]["color"][0], tracks, track_layer);
				redo["track"]["x1"].shift();
				redo["track"]["y1"].shift();
				redo["track"]["y2"].shift();
				redo["track"]["x2"].shift();
				redo["track"]["color"].shift();
				console.log("Redo track")
			}
			if (redo["type"][0] === "node") {
				var qq = find(img, redo["node"]["img"][0]);
				if (qq === -1) {
					addNode(redo["node"]["x"][0], redo["node"]["y"][0], node_layer, nodes, 10, redo["node"]["color"][0], redo["node"]["text"][0])

				} else {
					addNode(redo["node"]["x"][0], redo["node"]["y"][0], node_layer, nodes, 10, redo["node"]["color"][0], redo["node"]["text"][0], qq)
				}
				redo["node"]["x"].shift();
				redo["node"]["y"].shift();
				redo["node"]["color"].shift();
				redo["node"]["text"].shift();
				redo["node"]["img"].shift();
				console.log('Redo node');
			}
			redo["type"].shift();
			paper.view.draw();
		}

	}

	function find(array, value) {
		for (var i = 0; i < array.length; i++) {
			if (array[i] == value) return i;
		}
		return -1;
	}

	function compareNumeric(a, b) {
		if (a > b) return -1;
		if (a < b) return 1;
	}
	var Command = function(execute, undo, redo, value) {
		this.execute = execute;
		this.undo = undo;
		this.redo = redo;
		this.value = value;
	}
	function DeleteNode(NodeSelected, TrackSelected) {
		var items = project.getItems({
			class: Path
		});
		for (var i in items) {
			if ((NodeSelected.position['x'] == items[i].segments[0].point.x) && (NodeSelected.position['y'] == items[i].segments[0].point.y)) {
				redo["track"]["x1"].push(tracks[items[i].id]["x1"]);
				redo["track"]["y1"].push(tracks[items[i].id]["y1"]);
				redo["track"]["x2"].push(tracks[items[i].id]["x2"]);
				redo["track"]["y2"].push(tracks[items[i].id]["y2"]);
				redo["track"]["color"].push(tracks[items[i].id]["color"]);
				redo["type"].push("track");
				delete tracks[items[i].id];
				items[i].remove();
			} else if ((NodeSelected.position['x'] == items[i].segments[1].point.x) && (NodeSelected.position['y'] == items[i].segments[1].point.y)) {
				redo["track"]["x1"].push(tracks[items[i].id]["x1"]);
				redo["track"]["y1"].push(tracks[items[i].id]["y1"]);
				redo["track"]["x2"].push(tracks[items[i].id]["x2"]);
				redo["track"]["y2"].push(tracks[items[i].id]["y2"]);
				redo["track"]["color"].push(tracks[items[i].id]["color"]);
				redo["type"].push("track");
				delete tracks[items[i].id];
				items[i].remove();
			}
		}
		if (typeof(TrackSelected.text) === "undefined") {
			redo["track"]["x1"].push(TrackSelected.segments[0].point.x);
			redo["track"]["y1"].push(TrackSelected.segments[0].point.y);
			redo["track"]["x2"].push(TrackSelected.segments[1].point.x);
			redo["track"]["y2"].push(TrackSelected.segments[1].point.y);
			redo["type"].push("track");
			delete tracks[TrackSelected.id]
			TrackSelected.remove();

		} else {
			redo["node"]["text"].push(nodes[NodeSelected]["text"]);
			redo["node"]["color"].push(nodes[NodeSelected]["color"]);
			redo["node"]["x"].push(nodes[NodeSelected]["x"]);
			redo["node"]["y"].push(nodes[NodeSelected]["y"]);
			redo["type"].push("node");
			NodeSelected.remove();
			NodeSelected.text.remove();
			delete nodes[NodeSelected];
		}
		paper.view.draw();
	}
	function deleteAll(node_layer, track_layer, nodes, tracks) {
		new_node.remove();
		new_track.remove();
		node_layer.clear();
		track_layer.clear();
		nodes = {};
		tracks = {};
		view.draw();
		console.log(nodes)
	}

	$('#myCanvas').mousewheel(function() {
		var z = paper.view.zoom;
		var kart = paper.view.zoom;
		if (event.deltaY < 0) {
			if (z >= 0.2) paper.view.zoom = z - 0.1;
		} else {
			if (z <= 2) paper.view.zoom = z + 0.1;
		}
	});
	$('#draw_node').on('click', function(event) {
		var color = document.getElementById('id_color').value;
		var text = document.getElementById('id_text').value;
		addNode(cursor.position['x'], cursor.position['y'], node_layer, nodes, 10, color, text);
	});
	$('#DeleteAll').on('click', function(){
		deleteAll(node_layer, track_layer, nodes, tracks)
	});
	addNode(254, 555, node_layer, nodes, 10, 'black', 'Name');
	addNode(544, 277, node_layer, nodes, 10, 'black', 'Name 1');
	addTrack(254, 555, 544, 277, 'green', tracks, track_layer);
	addNode(523, 377, node_layer, nodes, 10, 'black', 'Name 2');
	addNode(99, 222, node_layer, nodes, 10, 'black', 'Name 3');
	addTrack(523, 377, 99, 222, 'gray', tracks, track_layer);
	addTrack(254, 555, 523, 377, 'blue', tracks, track_layer);
	addTrack(254, 555, 99, 222, 'red', tracks, track_layer);
	addTrack(544, 277, 523, 377, 'blue', tracks, track_layer);
	addNode(652, 200, node_layer, nodes, 10, 'black', 'Name 4', 0);
	addNode(400, 500, node_layer, nodes, 10, 'black', 'Name 5', 0);

	$('#DeleteThis').on('click', function(event) {
		DeleteNode(NowSelected, NowSelectedTrack)
	});
	$('#MoveThis').on('click', function(event) {
		move = true;
	});

});