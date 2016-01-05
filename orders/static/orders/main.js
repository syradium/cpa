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
		{footerFormatter: totalFormatter, field: field, title: title},
		{footerFormatter: sumFooterFormater('clicks'), title: 'Кликов'},
		{footerFormatter: sumFooterFormater('cr'), title: 'CR'},
		{footerFormatter: sumFooterFormater('approved'), formatter: 'approvedFormatter', title: 'Одобрено'},
		{footerFormatter: sumFooterFormater('accepted'), field: 'accepted', title: 'Принято'},
		{footerFormatter: sumFooterFormater('processing'), field: 'processing', title: 'Ожидает'},
		{footerFormatter: sumFooterFormater('canceled'), field: 'canceled', title: 'Отменено'},
		{footerFormatter: sumFooterFormater('total'), field: 'total', title: 'Всего'},
		{footerFormatter: sumFooterFormater('sum_total', undefined, priceFormatter), field: 'sum_total', formatter: 'priceFormatter', title: 'Сумма'},
		{footerFormatter: sumFooterFormater('sum_paid', undefined, priceFormatter), field: 'sum_paid', formatter: 'priceFormatter', title: 'Оплачено'},
	];

	$('#statistics').bootstrapTable('destroy').bootstrapTable({
		responseHandler: statisticsResponseHandler(fieldExtractor, field),
		columns: statisticsCols,
		showRefresh: true,
		showFooter: true
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
	return moment.utc(value.created_on).format('DD.MM.YY HH:MM');
}

function statisticsResponseHandler(groupby_key_func, key_name) {
	return function(res) {
		response = {};
		res.map(function(a) {
			var key = groupby_key_func(a[key_name]);

			if(!(key in response))
				response[key] = {sum_paid: 0, sum_total: 0, total: 0, accepted: 0, canceled: 0, processing: 0};

			var payment_status_mapping = {'-1': 'canceled', '0': 'processing', '1': 'accepted'};
			var status = payment_status_mapping[a.data.payment_status];
			var x = response[key][status];
			response[key][status] = (x === undefined) ? 1 : x + 1;

			if(a.data.payment_status == "1")
				response[key].sum_paid += Number.parseInt(a.data.payment_sum || 0);

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
	return moment.utc(timestamp).format('DD.MM.YYYY');
}

function priceFormatter(value, row) {
	return value + ' ₽';
}

function approvedFormatter(value, row) {
	return (row.accepted / row.total * 100).toFixed(2) + '%';
}


function sumFooterFormater(field, parser, formatter) {
	return function(data) {
		var _parser = (parser === undefined ? Number.parseInt : parser)
		var _formatter = (formatter === undefined ? String : formatter)
		var result = data.reduce(function(previousValue, currentValue, currentIndex, array) {
			return previousValue + _parser(currentValue[field]);
		}, 0);
		return isNaN(result) ? '-' : _formatter(result);
	}
}


function totalFormatter(data) {
	return '<strong>Всего</strong>';
}
