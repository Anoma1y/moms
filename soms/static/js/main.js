	var selected = false; //Переменная для выбранного узла, false - по умолчанию узел не выбран
	var selected2 = false;
	var control_selected = false;
	var radius = 7; //радиус для круга
	var nodes = {}; //создание объекта "узел"
	var tracks = {}; //создание объекта "топология"
	var links = {}; //создание объекта "менеджер управления"
	var routes = {}; //создание объекта "путь"
	var graphs = []; //создание пустого массива "графа"
	var mode = "node"; //по умолчанию  = узел
	var text = true;
	var move = false;
	var drag = false;
	var thicknessRoute = 2;
	var drag_start = {};
	var drag_center = false;
	var node_color = 'red'; // цвет узла
	var node_selected_color = '#800'; // цвет выбраного узла
	var track_color = 'black'; // цвет топологии
	var route_color = 'green'; // цвет пути
	var link_color = 'blue'; //цвет контроля управления
	var thiknessNode = 1;
	var cursorColor = 'orange';
	var err = 'Error';
	var arrayIP = [];
	var arrIP = '';

	//установка библиотеки Paper JS в окне браузера
	paper.install(window);
	// Сделать глобальном, вводя его в окне
	// Функция, которая запустится после того, как страница полностью загрузится. Загрузка DOM-дерева
	$(document).ready(function() {
		$('body').on('contextmenu', '#networkmap', function(e) {
			return false;
		});
		//Настройка области (canvas) для рисования
		var canvas = document.getElementById('networkmap');
		paper.setup(canvas); // установка библиотеки paper и получения элемента карты по id canvas'a
		// $(document).height()
		paper.view.viewSize.height = $(document).height();  // размер области для рисования модели в высоту
		paper.view.viewSize.width = $(document).width();; // размер области для рисования модели в ширину
		console.log('Ширина области: ' + canvas.width);
		console.log('Высота области: ' + canvas.height);
		$("#print_control").click(function(){//Срабатывает при нажатие на кнопку P (id = print_control)
			var c = document.getElementById("networkmap");//Получает элемент по ID (networkmap)
			var dataString = c.toDataURL("image/png");//Сохраняет полученный элемент в разрешении PNG
			console.log('Screenshot complete');
    		window.open(dataString);//Открытие в новой вкладке нового скриншота
		});
		$('#screenshot').click(function(){	
			var c = document.getElementById("networkmap");//Получает элемент по ID (networkmap)
			var dataString = c.toDataURL("image/png");//Сохраняет полученный элемент в разрешении PNG
			// document.getElementById('img_bg').innerHTML = '<img src="https://cs541607.vk.me/c836122/v836122362/240ba/p7x4KXQTyZY.jpg" />';
			// document.getElementById('img_bg_1').innerHTML = '<img id="pic" src=' +dataString+ ' />';		

			$('#img_bg_1').css({
				// 'width': '100%',
				// 'height': '84%',
				'background-color': 'transparent',
			}); //Вставка изображения области канвас
			$("#control_img").load("{% url 'soms:update_for_model' networkmap.id %}");
			window.location.href = "#openModal"; //Открытие модального окна
			console.log('Ширина: ' + canvas.width);
			console.log('Высота: ' + canvas.height);
		});

		//Фоновое изображения для модели
		//Проверка (если изображение есть, то вставляется, если нету, то игнорируется)
		// функция для скришота модели
		{% if networkmap.images %}
			var backgroundURL = '{{ networkmap.images.url }}'; //URL фонового изображения
			var xx = 844,
				yy = 452;
			var centerIMG = new Raster({
				source: backgroundURL,
				position: new Point(xx,yy)
			});
			Raster.selected = false; //Выделение изображения (не работает)
			centerIMG.onLoad = function() {
				console.log('The image has loaded.');
			};
			{% endif %}
		//Добавление курсора
			var cursor = new Shape.Circle(paper.view.center, radius / 1.5); //Рисование курсора (точки размером радиус (7) / 1,5)
			$("#id_x").val(Math.round(cursor.position.x)); //Стандартное положение курсора (х)
			$("#id_y").val(Math.round(cursor.position.y)); //Стандартное положение курсора (y)
			{% if user.is_staff %} //Если пользователь в сети, то он будет видеть черную точку
					cursor.fillColor = cursorColor  //цвет заливки точки (cursorColor)
		{% endif %}  //черная точка видна только админу
			//Создание переменных для слоев
			var track_layer = paper.project.activeLayer; //Создание нового слоя для проекта и назначение его активным
			var route_layer = new Layer(); //Создание нового слоя
			var link_layer = new Layer(); //Создание нового слоя
			var node_layer = new Layer(); //Создание нового слоя
			var tool = new Tool(); //Создание инструмента
			// Обработка нажатия клавиш - горячие клавиши
			// функция onKeyDown принимает функцию по событию event
		tool.onKeyDown = function(event){
		//При нажатии клавиши a/ф вылезает окно по добавлению нового узла
		if(Key.isDown('a') || Key.isDown('ф')) 
		{
			// ((добавить выделение карты, чтобы не срабатывало при редактировании формы))
			if(move) move = false;
			if(mode == 'node')
			{
				$("#modify").load("{% url 'soms:node:add' %}", function(){
					$("#id_x").val(Math.round(cursor.position.x));
					$("#id_y").val(Math.round(cursor.position.y));
					$("#id_network_map [value='{{networkmap.id}}']").attr("selected", "selected");
					$("#id_network_map").parent().css('display', 'none');
				});
			}
	
		}
		else if(Key.isDown('f') || Key.isDown('а')) //Закрытие окон
		{
			$("#modify").load("{% url 'soms:update_for_model' networkmap.id %}");
		}
		else if(Key.isDown('s') || Key.isDown('ы'))
		{
			$('#modify').html("");
			if(selected)
			{
				selected.selected = false;
				selected = false;
			}
			if(selected2)
			{
				selected2.selected = false;
				selected2.fillColor = node_color;
				selected2 = false;
			}
			clearPath();
			paper.view.draw();
		}
	};
		//Cобытия перемещения круга по холсту за мышью, если зажата средняя кнопка мыши
		//Функция принимает событие event
		tool.onMouseDrag = function(event){
			if(!drag) return; // если мышкой перемещается то вернуть
			var dx = (event.event.pageX - drag_start.x) / paper.view.zoom; // переменная для перемещения по оси X
			var dy = (event.event.pageY - drag_start.y) / paper.view.zoom; // переменная для перемещения по оси Y
			paper.view.center = new Point( //  создание новой точки которая будет перемещаться
				drag_center.x - dx, // переменная для перемещения по оси X
				drag_center.y - dy  // переменная для перемещения по оси Y
			);
		};
		//Запрет перетаскивания при нажатой клавиши ЛКМ после нажатия ПКМ
		//Функция принимает событие event
		tool.onMouseUp = function(event){
			if(event.event.button == 2)  // проверка нажатие правой кнопкой мышки
			{
				drag = false;  // перетаскивание для ЛКМ запрещено
				console.log('Left click move = False');
			}
		};
		//Событие onmousedown по своему действию похоже на onclick и отличается от него тем, что срабатывает в момент нажатия на кнопку мыши.
		tool.onMouseDown = function(event)
		{
			var hitOptions = {stroke: true, fill: true}; //
			if (event.event.button == 0) { // если нажата ПКМ по узлу, то будет перемещение узла
				if (move && selected && !selected2) { //
					moveNode(selected, event.point); // при нажатии кнопки Переместить вызывается функция для переноса узла
					return;
				}
				if (mode == 'node') { // Если Узел
					cursor.position = event.point; // перемещение узла?
					$("#id_x").val(Math.round(cursor.position.x)); //Получения позиции курсора по координате Х
					$("#id_y").val(Math.round(cursor.position.y)); //Получения позиции курсора по координате У
				}
				else if (mode == 'track' || mode == 'route' || mode == 'link') { //Если это не узел, то выполняется другие функции (в данном случае выделение ЛКМ узлов при редактировании линий)
					var hitResult = paper.project.hitTest(event.point, hitOptions); //|| event.raster
					if (hitResult && hitResult.item && hitResult.item.className == 'Shape' || hitResult.item.className == 'Raster') { //|| hitResult.item.type == 'raster' добавлена возможность выделения ЛКМ узел с картинкой
						if (hitResult.item == selected) selected = false;//PointText
						selected2.selected = false;
						selected2.fillColor = node_color;
						selected2 = hitResult.item;
						selected2.selected = true;
						selected2.fillColor = node_selected_color;
						if ($("#track_add").length > 0) $('#add_control').click();
						else if ($('#track_update').length > 0) $('#update_control').click();
						else if ($('#track_delete').length > 0) $('#delete_control').click();
						else if ($("#route_add").length > 0) $('#add_control').click();
						else if ($('#route_update').length > 0) $('#update_control').click();
						else if ($('#route_delete').length > 0) $('#delete_control').click();
						else if ($('#link_add').length > 0) $('#add_control').click();
						else if ($('#link_delete').length > 0) $('#delete_control').click();
					}
				}
			}
			//Перемещение точки и выделение узлов только для админа
			//Запрет выделения для гостей
			{% if user.is_staff %}
			// Выделение узла если нажата ПКМ
			if (event.event.button == 2) 
			{
				if (move) move = false;
				if (mode == 'node') 
				{
					var hitResult = paper.project.hitTest(event.point, hitOptions);
					if (hitResult && hitResult.item && hitResult.item != cursor && hitResult.item.className != 'path' && hitResult.item.className != 'PointText') //point-text
					{
						paper.project.deselectAll();
						selected = hitResult.item;
						hitResult.item.selected = true;
						if ($("#node_add").length > 0) changeForm(selected);
						else if ($('#node_update').length > 0) $('#update_control').click();
						else if ($('#node_delete').length > 0) $('#delete_control').click();
					}
				}
				else if (mode == 'track' || mode == 'route' || mode == 'link') 
				{
					var hitResult = paper.project.hitTest(event.point, hitOptions);
					if (hitResult && hitResult.item.className == 'PointText') return; //upd. type - > className
					if (hitResult && hitResult.item) 
					{
						if (hitResult.item == selected2) 
						{
							selected2.fillColor = 'red';
							selected2 = false;
						}
						if (hitResult.item.className == 'path') //upd. type - > className
						{
							selected2.fillColor = 'node_color';
							selected2.selected = false;
							selected2 = false;
						}
						selected.selected = false;
						selected = false;
						selected = hitResult.item;
						hitResult.item.selected = true;
						console.log(selected.className)
						if ($("#track_add").length > 0) $('#add_control').click();
						else if ($('#track_update').length > 0) $('#update_control').click();
						else if ($('#track_delete').length > 0) $('#delete_control').click();
						else if ($("#route_add").length > 0) $('#add_control').click();
						else if ($('#route_update').length > 0) $('#update_control').click();
						else if ($('#route_delete').length > 0) $('#delete_control').click();
						else if ($('#link_add').length > 0) $('#add_control').click();
						else if ($('#link_delete').length > 0) $('#delete_control').click();
						else if ($('#networkmap_update').length > 0) $('#edit_model').click();//
					}
				}
			}
			{% endif %}
			if(event.event.button == 1) // перемещение средней кнопкой мышки
			{
				drag = true;
				drag_start.x = event.event.pageX;
				drag_start.y = event.event.pageY;
				drag_center = new Point(paper.view.center);
			}
			return false;
		};
		// функция добавления топологии с параметром track - топология, вызывается в форме по добавлению топологий
		function addTrack(track)
		{
			track_layer.activate();
			new_track = new Path();  // для новой топологии создается новый путь
			new_track.strokeColor = 'track_color';  // цвет задается переменой для который уже определен цвет
			new_track.add(new Point(nodes[track.fields.start_node].soms.fields.x,  // начало пути х,у
										nodes[track.fields.start_node].soms.fields.y));
			new_track.add(new Point(nodes[track.fields.end_node].soms.fields.x,  // конец пути х,у
									nodes[track.fields.end_node].soms.fields.y));
			new_track.soms = track;
			tracks[track.pk] = new_track;  // создается топология и ему назначается РК
		}
		// функция добавления менеджера управления
		function addLink(l)
		{ 
			link_layer.activate();
			new_link = new Path();
			new_link.strokeColor = link_color;
			new_link.add(new Point(nodes[l.fields.start_node].soms.fields.x, // начало пути х,у
									nodes[l.fields.start_node].soms.fields.y));
			new_link.add(new Point(nodes[l.fields.end_node].soms.fields.x, // конец пути х,у
									nodes[l.fields.end_node].soms.fields.y));
			new_link.soms = l;
			links[l.pk] = new_link;
		}
		// функция добавления пути с параметреами route - путь, вызывается в форме по добавлении пути
		function addRoute(route)
		{ 
			found = false;  //
			for(var i = 0; i < graphs.length; i++){
				graph = graphs[i]; //
				if(	(graph.soms.fields.start_node == route.fields.start_node &&
					graph.soms.fields.end_node == route.fields.end_node) ||
					(graph.soms.fields.start_node == route.fields.end_node &&
					graph.soms.fields.end_node == route.fields.start_node))
				{
					found = graphs[i];
					break;
				}
			}
			if(found)
			{
				found.soms.routes.push(route.pk);
				route.fields.graph = found;
			}
			else {
				route_layer.activate(); // активация слоя для рисования пути
				var new_graph;  // переменая для нового графа
				if(route.fields.start_node == route.fields.end_node){  // тут вроде добавления пути для 1 узла
					new_graph = new Path.Circle(new Point(nodes[route.fields.start_node].soms.fields.x, nodes[route.fields.start_node].soms.fields.y), radius + 3 ); // радиус нового узла
					new_graph.strokeColor = route_color; // цвет
				}
				else { // если 2 узла, то добавляется линия
					new_graph = new Path();  // для нового графа новый путь
					new_graph.strokeColor = route_color;  // цвет пути = цвету заданый в переменой
					new_graph.strokeWidth = thicknessRoute;
					new_graph.add(new Point(nodes[route.fields.start_node].soms.fields.x,  // добавления нового графа, начало графа х,у
					nodes[route.fields.start_node].soms.fields.y));
					new_graph.add(new Point(nodes[route.fields.end_node].soms.fields.x, // конец графа х,у
					nodes[route.fields.end_node].soms.fields.y));
				}
				new_graph.soms = {};  // новый граф пустой?
				new_graph.soms.routes = []; //
				new_graph.soms.fields = {'start_node':route.fields.start_node, 'end_node':route.fields.end_node}
				new_graph.soms.routes.push(route.pk); // добавления РК
				route.fields['graph'] = new_graph;
				graphs.push(new_graph);
			}
			routes[route.pk] = route;
		}
		//функция добавления нового узла с параметрами node - узел, вызывается в форме по добавлению узла
		function addNode(node)
		{
			node_layer.activate();  // активация слоя для узла
			var x = node.fields.x;  // координата по х, берется из формы для добавления по x
			var y = node.fields.y;  // координата по у, берется из формы для добавления по y
			var color = node.fields.color; //цвет узла
				var thiknessNode = node.fields.thickness //толщина узла
				var new_node;  // переменная для создания нового узла
				var node_type = node.fields.node_type;  // тип узла, берется из формы для добавления по типу (1, 2, 3)
				var img = {{ MEDIA_URL }}+node.fields.image; // изображения
				var img_node = '{% static "soms/" %}' + node.fields.image; //new переменная для добавления изображения узла из селект меню в форме
				if(node_type == 1 && node.fields.image === null)
				{
						new_node = new Shape.Rectangle(new Point(x - radius, y - radius), radius * thiknessNode);
				}
				else if(node_type == 1 && node.fields.image !== null)
				{
						new_node = new Raster(img_node, new Point(x,y));
				}
				if(node_type == 2 && node.fields.image === null)
				{
						new_node = new Shape.Circle(new Point(x, y), radius);
				}
				else if(node_type == 2 && node.fields.image !== null)
				{
						new_node = new Raster(img_node, new Point(x,y));
				}
				if(node_type == 3 && node.fields.image === null)
				{
						new_node = new Shape.Circle(new Point(x, y), radius / 1.5);
				}
				else if(node_type == 3 && node.fields.image !== null)
				{
						new_node = new Raster(img_node, new Point(x,y));
				}
				new_node.soms = node;//Привязка к модели
				if(node.fields.control_manager)// если контрол менеджер то круглик или квадратик по краям черный цвет
				{
						new_node.strokeColor = 'black';	 // цвет от края
					new_node.strokeWidth = 3;  // расстояние черного цвета от края
				}
				new_node.fillColor = color; // цвет узла, задается в определенной переменой node_color
				var text = new PointText();  // определяется переменная для добавления текста
				text.content = node.fields.name;  // присваивание имени для узла
				text.position = new Point(x, y + (radius * thiknessNode) + 3);  // имя узла на опред. расстоянии
				new_node.soms.text = text;  // добавляется текст
				nodes[node.pk] = new_node; // создается узел с определенным РК

			}	

			//Функция, при нажатии на кнопку "Изменить", откроется форма для изменения узла или связей
			$("#update_control").click(function(){
				if(move) move = false;
				if(mode == 'node')
				{
		
						$("#modify").load("{% url 'soms:node:index' %}"+selected.soms.pk+"/");
						console.log('Open update control for node');
				}
				if(mode == 'track')
				{
					if(selected && selected.type == 'path')
						$("#modify").load("{% url 'soms:track:index' %}"+selected.soms.pk+"/");
					else $('#modify').html("");
				}
			});

			///////////РЕДАКТИРОВАНИЕ КАРТЫ///////////////
			$('#edit_model').click(function() {
					$("#modify").load("{% url 'soms:update_for_model' networkmap.id %}");
			});

			//Функция для перемещения узлов по карте
			$("#move_control").click(function(){//Срабатывает при нажатии на кнопку Переместить (id = move_control)
				$('#modify').html("");
				if(!selected) return;//Если ничего не выделено, то вернуть
				if(selected2) selected2.selected = false; //Если выделен то перевести обратно в False
				selected2 = false; //После повторного нажатие на пустые участки карты ПКМ, переводит в False
				move = true;//Переводит переменную в True, для перемещения узла
				paper.view.draw();//Перерисовка
			});

			//Функция для вызова форм для добавления новых узлов, связей, топологий и т.п.
			$("#add_control").click(function(){//Вызывается при нажатии на кнопку Добавить (id = add_control)
				if(move) move = false; //
				if(mode == 'node') //Если в редакторе выбран узел, то для узла срабатывает if
				{
					$("#modify").load("{% url 'soms:node:add' %}", function(){//При нажатии на кнопку Добавить, загружается форма по ссылке и  вызывается функция
						$("#id_x").val(Math.round(cursor.position.x));//Для поля X получает координаты по Х, при нажатии на карту
						$("#id_y").val(Math.round(cursor.position.y));//Для поля Y получает координаты по Y, при нажатии на карту
						$("#id_network_map [value='{{networkmap.id}}']").attr("selected", "selected");
						$("#id_network_map").parent().css('display', 'none');
					});
				}
				if(mode == 'track')//Если в редакторе выбрана связь, то для связи срабатывает if
				{
					if(!selected || !selected2){
						$('#modify').html("");
						return;
					}
					$("#modify").load("{% url 'soms:track:add' networkmap.id %}", function(){
						$("#id_start_node [value='"+selected.soms.pk+"']").attr("selected", "selected");
						$("#id_end_node [value='"+selected2.soms.pk+"']").attr("selected", "selected");
						$("#id_start_node").parent().css('display', 'none');
						$("#id_end_node").parent().css('display', 'none');
					});
				}
				if(mode == 'link')
				{
					if(!selected || !selected2 || selected.soms.fields.control_manager == false){
						$('#modify').html("");
						return;
					}
					$("#modify").load("{% url 'soms:link:add' networkmap.id %}", function(){
						$("#id_start_node [value='"+selected.soms.pk+"']").attr("selected", "selected");
						$("#id_end_node [value='"+selected2.soms.pk+"']").attr("selected", "selected");
						$("#id_start_node").parent().css('display', 'none');
						$("#id_end_node").parent().css('display', 'none');
					});
				}
				if(mode == 'route')
				{
					var fpk;
					if(!selected){
						$('#modify').html("");
						return;
					}
					else if(!selected2){
							fpk = selected.soms.pk;
					}
					else fpk = selected2.soms.pk;
					console.log(selected.soms.pk+"/"+fpk+"/");
					$("#modify").load("{% url 'soms:route:add' %}"+selected.soms.pk+"/"+fpk+"/", function(){
					});
				}
			});
			//Функция для показа/скрытия текста
			$("#text_control").click(function(){// Срабатывает при нажатии на кнопку Т (id = text_control)
				text = !text; //True != True
				for(node in nodes) {//Проверка узла в узлах
					if(text) nodes[node].soms.text.visible = true;//Если текст присутствует, эта переменная равна True
					else nodes[node].soms.text.visible = false;//Иначе переводит в False (не видно текста)
				}
				paper.view.draw();//Перерисовка
			});
			// // функция для скришота модели
			// $("#print_control").click(function(){//Срабатывает при нажатие на кнопку P (id = print_control)
				// 	var c = document.getElementById("networkmap");//Получает элемент по ID (networkmap)
				// 	var dataString = c.toDataURL("image/png");//Сохраняет полученный элемент в разрешении PNG
				// 	window.open(dataString);//Открытие в новой вкладке нового скриншота
			// });
			//Функция закрывания всех активных форм (при нажатии на Х)
			$("#close_control").click(function(){ //Срабатывает при нажатие на кнопку X (id = close_control)
				$('#modify').html("");//Если
				if(selected){ //Если выделен узел, то все выделение будет снято
					selected.selected = false; //Если True, то будет равно False
					selected = false; //Если True, то будет равно False
				}
				if(selected2){
					selected2.selected = false; //Если True, то будет равно False
					selected2.fillColor = node_color; //Выделенный узел изменит свой цвет на стандартный
					selected2 = false; //Если True, то будет равно False
				}
				clearPath();//Очистка
				paper.view.draw();//Перерисовка
			});
			//функция работает при нажатии на кнопку submit и только для изменения мапы, далее вызывает функцию и т.п.
			$(document).on('submit', '#networkmap_update', function(){
				var fd = new FormData; //формдата
			fd.append('img', $input.prop('files')[0]); //позволяет загружать картинки и изменять модель
				id = $(this).attr('id');  // при нажатии на форму, будет вызываться функции по id()
				$.ajax({  // метод аякс
					//dataType: 'json',
					url: $(this).attr('action'),
					data: $(this).serialize(),
					data: fd, //хз чо за переменная
					type: 'POST',  // тип POST
					async: true, //синхронизация
					enctype: "multipart/form-data",
					//дальше не работает, но если удалить гг всему.
					success: function(response, status, xhr){ // при срабатывании функции передаються 3 параметра(ответ, статус и ...)
						// console.log(data)
						var ct = xhr.getResponseHeader("content-type") || "";
						if(ct.indexOf('json') > -1) {
						if(id == 'networkmap_update')
							{
								clearAll();
								initAll();
								return false;
							}
						$('#modify').html("");
								paper.view.draw();	 // рисование с помощью библиотеки paper
						}
					}
				});
				return false;
			});
			$(document).on('submit', 'form', function(){
				// var $input = $("file");
				// var fd = new FormData;
				// fd.append('img', $input.prop('files')[0]);
				id = $(this).attr('id');  // при нажатии на форму, будет вызываться функции по id()
				$.ajax({  // метод аякс
					//dataType: 'json',
					url: $(this).attr('action'),
					data: $(this).serialize(),
					type: 'POST',  // тип POST
					async: true,
					enctype: "multipart/form-data",
					success: function(response, status, xhr){ // при срабатывании функции передаються 3 параметра(ответ, статус и ...)
						// console.log(data)
						var ct = xhr.getResponseHeader("content-type") || "";
						if(ct.indexOf('html') > -1) {
							$("#modify").html(response);
							$("#id_network_map").parent().css('display', 'none');
							$("#id_start_node").parent().css('display', 'none');
							$("#id_end_node").parent().css('display', 'none');
						}
						if(ct.indexOf('json') > -1) {
							if(id == 'node_add') // при нажатии на добавить узел вызов функций добавление узла
							{
								addNode(response[0])
								console.log('Node add');
							}
							if(id == 'node_update')  // вызов функции изменения узла
							{
								clearAll();
								initAll();
								console.log('Node update');
								return false;
							}
							// if(id == 'networkmap_update')
							// {
								// 	clearAll();
								// 	initAll();
								// 	return false;
							// }
						if(id == 'node_delete')
							{ // вызов функции удаления узла
								clearAll();
								initAll();
								return false;
							}
							if(id == 'track_add')
							{ // вызов функции добавления топологии
								addTrack(response[0]);
							}
							if(id == 'link_add')
							{ // вызов функции добавления менеджера управления
								addLink(response[0]);
							}
							if(id == 'track_update')
							{ // вызов функции обновления топологии
								tracks[response[0].pk].soms = response[0];
							}
							if(id == 'track_delete')
							{ // вызов функции удаления топологии
								removeTrack(control_selected.soms);
							}
							if(id == 'link_delete')
							{ // вызов функции удаления менеджера управления
								removeLink(control_selected.soms);
							}
							if(id == 'route_add')
							{ // вызов функции добавления пути
								addRoute(response[0]);
							}
							if(id == 'route_delete')
							{ // вызов функции удаления пути
								clearRoute();
								initRoute();
								return false;
							}
							$('#modify').html("");
								paper.view.draw();	 // рисование с помощью библиотеки paper
						}
					}
				});
				return false;
			});
			//Функция для рандома от min значения до max значения
			function randomInt(min, max) {
				var rand = min - 0.5 + Math.random() * (max - min + 1)
				rand = Math.round(rand);
					return rand;
			}
			var aaa = [];
			var id_node = [];
			var node_type = [];
			var name_node = [];
			{% for node in q %}
				aaa.push('{{ node.ip }}');
				id_node.push('{{ node.id }}');
				name_node.push('{{ node.name }}');
				node_type.push('{{ node.node_type }}');
			{% endfor %}
			//Функция для генерации IP-адреса и проверки наличия
			function CheckRandomIP() {
				function randomIP(){
					function random(){
						return (1+(Math.random()*255))|0 
					}
					return [random(),random(),random(),random()].join(".");
				}
				function checkArray(originalArr, checkArr){
				    for(var i=0; i<checkArr.length; i++){
				        if(originalArr.indexOf(checkArr[i]) == -1) return false;
				    }
				    return true;
				}
				var IP = [], 
					sd = [];
				var jj = randomIP(), 
					jq = randomIP();
				var rand = IP.push(jj), 
					rand = sd.push(jq);  
				if (checkArray(aaa, IP) === false) {
					return jj;
				}
				else if (checkArray(aaa, IP) === true) {
					return jq;
				} 
			}

			//Функция автозаполнения 
			$(document).on('click', '#default_control', function(){
				if(mode == 'node')  //Автозаполнения для узла
				{
					var element = {
						soms: //Узел
						{
							fields: //Поля
							{
								thickness: 1, //new толщина узла
								popularity: randomInt(1,100), //популярность узла
								cpu: randomInt(1,100), //нагрузка на процессор
								ip: CheckRandomIP(), //IP
								output_bandwidth: randomInt(1,100),//исходящая ширина канала
								input_bandwidth: randomInt(1,100),//входящая ширина канала
								users: randomInt(1,100),//количество пользователей
								memory: randomInt(1,100),//память
								max_users: randomInt(1,100),//максимальное число пользователей
								node_type: 1,//типа узла 1 - Репликатор, 2 - Ретранслятор, 3 - Узел
							}
						}
					};
					changeForm(element); //Обработать форму
					console.log('AutoComplete Node');
				}
			});
			
			function changeForm(element)
			{
				if(mode == 'node')
				{
					for(field in element.soms.fields)
					{
						var value = element.soms.fields[field];
						//new удален ip из игнора для автозаполнения
						if($.inArray(field, ['name', 'x', 'y']) != -1) continue;
						if($('#id_' + field).attr('type') == 'checkbox')
						{
							if(value)
								$('#id_' + field).prop('checked', 'checked');
							else
								$('#id_' + field).prop('checked', null);
						}
						$('#id_' + field).val(value);
					}
				}
			}

			//функция для перемещение узла с 2 параметрами(узел и точка куда нужно переместить)
			function moveNode(node, point)
			{
				// координата точки х
				x = Math.round(point.x);
				// координата точки у
				y = Math.round(point.y); 
				//jquery метод getJSON
				//получения url представления для перемещение узла
				$.getJSON("{% url 'soms:node:move' %}"+node.soms.pk+"/"+x+"/"+y+"/", function(response){ 
						node.position = point; // текущая позиция узла=точка
						node.soms.text.position = new Point(point.x, point.y + radius * 2); // при перемещении сохраняется расположение текста
						for(track in tracks){  // перемещение для топологии
							if(tracks[track].soms.fields.start_node == node.soms.pk)
							tracks[track].segments[0].point = point; // начало узла топологии по РК
							if(tracks[track].soms.fields.end_node == node.soms.pk)
							tracks[track].segments[1].point = point; // конец узла топологии по РК
						}
						for(track in links){ // для менеджера управления
							if(links[track].soms.fields.start_node == node.soms.pk)
							links[track].segments[0].point = point;
							if(links[track].soms.fields.end_node == node.soms.pk)
							links[track].segments[1].point = point;
						}
						for(graph in graphs){ // для графов
							if(graphs[graph].soms.fields.start_node == node.soms.pk)
							{
								if(graphs[graph].soms.fields.start_node == graphs[graph].soms.fields.end_node)
									graphs[graph].position = point;
								else graphs[graph].segments[0].point = point;
							}
							if(graphs[graph].soms.fields.end_node == node.soms.pk)
							{
								if(graphs[graph].soms.fields.start_node == graphs[graph].soms.fields.end_node)
									graphs[graph].position = point;
								else graphs[graph].segments[1].point = point;
							}
						}
						node.soms.fields.x = point.x;
						node.soms.fields.y = point.y;
				});
			}

			//функция для удаления узла (не используется)
			function removeNode(node)
			{
				nodes[node.pk].soms.text.remove();  // удаление узла по PK
				nodes[node.pk].remove();
				delete nodes[node.pk];
				console.log('Node removed');
			}

			//Функция удаление топологии между узлами (параметр track)
			function removeTrack(track)
			{
				tracks[track.pk].remove();  // удаление топологии по РК
				delete tracks[track.pk]; // удалется топология с РК
				console.log('Track removed');
			}
			//Функция удаление менеджера управления
			function removeLink(l)
			{ 
				links[l.pk].remove();
				delete links[l.pk];
				console.log('Link removed');
			}

			//Функция удаления пути между связями (параметр element, route)
			function removeRoute(element, route)
			{ 
				var index = element.soms.routes.indexOf(route.pk)
				element.soms.routes.splice(index, 1);
				if(element.soms.routes.length == 0) element.remove();
				delete routes[route.pk];
				console.log('Route removed');
			}

			//Функция очистки пути
			function clearPath()
			{
				for(i = 0; i < graphs.length; i++)
					graphs[i].strokeColor = route_color;
			}

			//Функция рисовки
			function drawPath(path)
			{ // ?
				for(i = 0; i < path.length; i++) {
					routes[path[i]].fields.graph.strokeColor = '#00F';
				}
			}

			// при нажатии кнопки изменения на докумете с id=id_parent вызываеться функция для изменения родительского узла?
			$(document).on('change', "#id_parent", function(){ 
				var index = $(this).val();
				if(index == ""){
					$('#id_quality').val("");
					$('#id_bandwidth').val("");
					$('#id_name').val("");
					console.log(selected);
					if(selected.soms.fields.node_type == 1)
					{
						$('#id_quality').prop('readonly', false);
						$('#id_bandwidth').prop('readonly', false);
						$('#id_name').prop('readonly', false);
					}
					clearPath();
						paper.view.draw();
					return;
				}
				$.getJSON("{% url 'soms:route:detail' %}" + index, function(data){
					clearPath();
					drawPath(data);
					$('#id_quality').val(routes[index].fields.quality);
					$('#id_bandwidth').val(routes[index].fields.bandwidth);
					$('#id_name').val(routes[index].fields.name);
					if(selected2){
						$('#id_quality').prop('readonly', true);
						$('#id_bandwidth').prop('readonly', true);
						$('#id_name').prop('readonly', true);
					}
						paper.view.draw();
				});
			});

			$("#mode").change(function(){
				mode = false;
				clearPath();
				for(node in nodes) {
					nodes[node].visible = true;
					if(text) nodes[node].soms.text.visible = true;
					else nodes[node].soms.text.visible = false;
				}
				for(track in tracks) tracks[track].visible = false;
				for(graph in graphs) graphs[graph].visible = false;
				for(l in links) links[l].visible = false;
				cursor.visible = true;
				mode = $(this).val();
				if(mode == 'node'){
				}
				else if(mode == 'track'){
					for(track in tracks) tracks[track].visible = true;
					cursor.visible = false;
				}
				else if(mode == 'link'){
					for(l in links) links[l].visible = true;
					for(node in nodes)
						if(nodes[node].soms.fields.node_type == 3) {
								nodes[node].visible = false;
							nodes[node].soms.text.visible = false;
						}
					cursor.visible = false;
				}
					else if(mode == 'route'){
					for(node in nodes)
						if(nodes[node].soms.fields.node_type == 3) {
								nodes[node].visible = false;
							nodes[node].soms.text.visible = false;
						}
					for(graph in graphs) graphs[graph].visible = true;
					cursor.visible = false;
				}
				paper.project.deselectAll();
				selected = false;
				selected2 = false;
				$('#modify').html("");
					paper.view.draw();
			});

			//Функция для удаления объектов с карты сети
			$("#delete_control").click(function(){
				//если узел находиться в движение (перемещение) то остановить его
				if(move){
					move = false;
				}
				//для узла
				if(mode == 'node')
				{
					//проверка выделения узла
					if(selected)
					{
						//загрузка формы для удаления узла
						$("#modify").load("{% url 'soms:node:index' %}"+selected.soms.pk+"/delete/");
						control_selected = selected;
					}
					//иначе ничего не происходит
					else $('#modify').html("");
				}
				//для топологии
				else if(mode == 'track') {
					//проверка выделения топологии
					if(selected && selected.className == 'Path') //upd. type - > className
					{
						//загрузка формы для удаления топологии
						$("#modify").load("{% url 'soms:track:index' %}"+selected.soms.pk+"/delete/");
						control_selected = selected;
					}
					else $('#modify').html("");
				}
				//для менеджера управления
				else if(mode == 'link') {
					//проверка выделения менеджера управления
					if(selected && selected.className == 'Path') //upd. type - > className
					{
						//загрузка формы для удаления менеджера управления
						$("#modify").load("{% url 'soms:link:index' %}"+selected.soms.pk+"/delete/");
						control_selected = selected;
					}
					else $('#modify').html("");
				}
				//для маршрутов
				else if(mode == 'route')
				{
					//проверка выделения маршрута
					if(selected && selected.className == 'Path') //upd. type - > className
					{
						//загрузка формы для удаления маршрута
						$("#modify").load("{% url 'soms:route:delete' %}"+selected.soms.fields.start_node+"/"+selected.soms.fields.end_node+"/");
						control_selected = selected;
					}
					else $('#modify').html("");
				}
			});


			initAll();
			//функция вызова формы редакторов
			//Запрашивает JSON-данные у сервера, методом GET.
			//$.getJSON( url [, data] [, success(data, textStatus, jqXHR)] )
			//url - адрес, на который отправляется запрос. (строка)
			//data - данные,  отправляемые на сервер в виде формате map (наборы ключ:значение) или string (строка) (объект)
			//success(data, textStatus, jqXHR) - функция, вызываемая при успешном завершении ajax-запроса. (функция)
			//Данные отправляются через URL как часть строки запроса.
			//Если представляют из себя объект, то он будет преобразован в строку и закодирован для передачи через URL.
			function initAll() {  //функция инициализации объектов на карте, все объекты хранятся в JSON формате
				$.getJSON("{% url 'soms:networkmap_node_json' networkmap.id %}", function(data){  // вызывает представление формы узла
						for(i = 0; i < data.length; i++) { //для каждого i от 0 до длины строки данных отправленных при вызове функции
							addNode(data[i]); //вызов функции addNode (получает каждый узел) и добавляет его на карту
							// console.log(data[i].fields.ip);
							// arrayIP.push(data[i].fields.ip);
							console.log( "Node successfully loaded" ); //выведет суксес если все узлы загрузились норм
						}
						$.getJSON("{% url 'soms:networkmap_track_json' networkmap.id %}", function(data){  // вызывает представление формы топологии
							for(i = 0; i < data.length; i++) { //для каждого i от 0 до длины строки данных отправленных при вызове функции
								addTrack(data[i]); //вызов функции addTrack (получает каждая связь) и добавляет его на карту
							}
							$.getJSON("{% url 'soms:networkmap_route_json' networkmap.id %}", function(data){  // вызывает представление  форма пути
								for(i = 0; i < data.length; i++) {//для каждого i от 0 до длины строки данных отправленных при вызове функции
									addRoute(data[i]);//вызов функции addRoute (получает каждая линия топологии) и добавляет его на карту
								}
								$.getJSON("{% url 'soms:networkmap_link_json' networkmap.id %}", function(data){  // вызывает представление  форма менеджера управления
									for(i = 0; i < data.length; i++) {//для каждого i от 0 до длины строки данных отправленных при вызове функции
										addLink(data[i]);//вызов функции addLink (получает каждый менеджер управления) и добавляет его на карту
									}
									$("#mode").change();//Событие change происходит по окончании изменении значения элемента формы, когда это изменение зафиксировано.
								});//закрываю скобочку
							});//закрываю скобочку
						});//закрываю скобочку
				});//закрываю скобочку
			}//функция закрыта

			// функция инициализации маршрута
			function initRoute()
			{  
				$.getJSON("{% url 'soms:networkmap_route_json' networkmap.id %}", function(data){
					for(i = 0; i < data.length; i++) {
						addRoute(data[i]);
					}
					$("#mode").change();
				});
			}
			//очистка всего
			function clearAll()
			{
				//удалить все узлы и текст к узлам
				for(node in nodes) { 
					nodes[node].remove();
					nodes[node].soms.text.remove();
				}
				//удалить все топологии
				for(track in tracks) {
					tracks[track].remove();
				}
				//удалить все графы
				for(graph in graphs) {
					graphs[graph].remove();
				}
				//создание (обновление) пустых объектов
				nodes = {};
				tracks = {};
				routes = {};
				graphs = [];
			}

			//очистка (обновление) путей
			function clearRoute()
			{
				for(graph in graphs) graphs[graph].remove();
				routes = {};
				graphs = [];
			}

			//функция для увеличения карты колесиком мышки (зумирование)
			$('#networkmap').mousewheel(function()
			{
				var z = paper.view.zoom; //зумирование
				var kart = paper.view.zoom;
				if(event.deltaY < 0) { //количество прокрученных пикселей по горизонтали и вертикали
					if(z >= 0.2) paper.view.zoom = z - 0.1;  // мин и макс значения зумирования
				}
				else {
					if(z <= 2) paper.view.zoom = z + 0.1;  // мин и макс значения зумирования
				}
			});

		});