$(function() {
	createStatsTable('created_on', 'Дата');

	$('.group-button').click(function() {
		var field = $(this).data('group-field');
		if(field == 'order_id')
			createOrderTable('#statistics');
		else
			createStatsTable(field, $(this).data('group-title'));
		$(this).removeClass('btn-link').addClass('btn-info').siblings('.group-button').removeClass('btn-info').addClass('btn-link');
	});

	$('#from_date, #to_date').datepicker({dateFormat: "yy-mm-dd"});
	$('.filter-by-date').click(function() {
		var from_date = $('#from_date').val();
		var to_date = $('#to_date').val();
		if(!from_date && !to_date)
			return;
		$('#statistics').bootstrapTable('refresh', {'query': {'created_on__gte': from_date, 'created_on__lte': to_date}});
	});
});


function createOrderTable(selector) {
	var order_columns  = [
		{field: 'order_id', title: 'ID'},
		{formatter: dateFormatter, title: 'Дата'},
		{field: 'domain', title: 'Домен'},
		{field: 'price', title: 'Цена'},
		{field: 'data', formatter: dataFormatter('status'), title: 'Статус'},
		{field: 'data', formatter: dataFormatter('name'), title: 'Имя'},
		{field: 'data', formatter: dataFormatter('phone'), title: 'Телефон'},
		{field: 'data', formatter: dataFormatter('payment_sum'), title: 'Сумма оплаты'},
		{field: 'data', formatter: dataFormatter('payment_status'), title: 'Статус оплаты'},
		{field: 'utm_source', title: 'UTM source'},
		{field: 'utm_campaign', title: 'UTM campaign'},
		{field: 'utm_content', title: 'UTM content'},
		{events: 'window.operateEvents', formatter: actionsFormatter, title: 'Действия'},
	];

	window.operateEvents = {
		'click .remove': function (e, value, row, index) {
			$order_list.bootstrapTable('removeByUniqueId', row.pk);
			e.preventDefault();
		}
	};

	var $order_list = $(selector).bootstrapTable('destroy').bootstrapTable({
		columns: order_columns,
		pageSize: 25,
		pageList: '[50, 100, 250, All]',
		showRefresh: true
	}).on('post-body.bs.table', function () {
		Intercooler.processNodes($('.action'));
	});

}

function createStatsTable(field, title, fieldExtractor) {
	if(field == 'created_on')
		fieldExtractor = extractDate;
	else
		fieldExtractor = function(value) { return value; }

	var statisticsCols = [
		{field: field, title: title},
		{title: 'Кликов'},
		{title: 'CR'},
		{formatter: 'approvedFormatter', title: 'Одобрено'},
		{field: 'accepted', title: 'Принято'},
		{field: 'processing', title: 'Ожидает'},
		{field: 'canceled', title: 'Отменено'},
		{field: 'total', title: 'Всего'},
		{field: 'sum_total', formatter: 'priceFormatter', title: 'Сумма'},
		{field: 'sum_paid', formatter: 'priceFormatter', title: 'Оплачено'},
	];

	$('#statistics').bootstrapTable('destroy').bootstrapTable({
		responseHandler: statisticsResponseHandler(fieldExtractor, field),
		columns: statisticsCols,
		showRefresh: true
	});
}

function actionsFormatter(row, value) {
	return '<a href="#" class="action remove" ic-delete-from="/api/orders/' + value.pk + '/">Удалить</a>'
}

function dataFormatter(field) {
	return function(row, value) {
		return value['data'][field];
	}
}

function dateFormatter(row, value) {
	return moment.utc(value.created_on).local().format('DD.MM.YY HH:MM');
}

function statisticsResponseHandler(groupby_key_func, key_name) {
	return function(res) {
		response = {};
		res.map(function(a) {
			var key = groupby_key_func(a[key_name]);
			if(!(key in response))
				response[key] = {sum_paid: 0, sum_total: 0, total: 0, accepted: 0};

			/*
			if(a.data.status !== undefined)
			{
				var x = response[key][a.data.status];
				response[key][a.data.status] = (x === undefined) ? 1 : x + 1;
			}
			*/
			var payment_status_mapping = {'-1': 'canceled', '0': 'processing', '1': 'accepted'};
			var status = payment_status_mapping[a.data.payment_status];
			var x = response[key][status];
			response[key][status] = (x === undefined) ? 1 : x + 1;

			if(a.data.status == "1")
				response[key].sum_paid += a.price;
			response[key].sum_total += a.price;
			response[key].total += 1;
		});
		return $.map(response, function(value, index) {
			value[key_name] = index ? index: 'Неопределен';
			return value;
		});
	}
}

function extractDate(timestamp) {
	return moment.utc(timestamp).local().format('DD.MM.YYYY');
}

function priceFormatter(value, row) {
	return value + ' ₽';
}

function approvedFormatter(value, row) {
	return row.accepted / row.total * 100 + '%';
}
