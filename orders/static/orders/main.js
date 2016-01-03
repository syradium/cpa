$(function() {
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
	{field: 'data', formatter: dataFormatter('utm1'), title: 'Utm source'},
	{field: 'data', formatter: dataFormatter('utm2'), title: 'Utm campaign'},
	{field: 'data', formatter: dataFormatter('utm3'), title: 'Utm content'},
	{field: 'data', formatter: dataFormatter('utm4'), title: 'Utm term'},
	{events: 'window.operateEvents', formatter: actionsFormatter, title: 'Действия'},
	];

	window.operateEvents = {
		'click .remove': function (e, value, row, index) {
			$order_list.bootstrapTable('removeByUniqueId', row.pk);
			e.preventDefault();
		}
	};

	var $order_list = $('#orderList').bootstrapTable({
		columns: order_columns,
		pageSize: 25,
		pageList: '[50, 100, 250, All]',
		showRefresh: true
	}).on('post-body.bs.table', function () {
		Intercooler.processNodes($('.action'));
	});

	var $statistics = $('#statistics').bootstrapTable();
});

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

function statisticsResponseHandler(res) {
	response = {};
	res.map(function(a) {
		var date = extractDate(a.created_on);
		if(!(date in response))
			response[date] = {sum_paid: 0, sum_total: 0, total: 0, accepted: 0};

		if(a.data.status !== undefined)
		{
			var x = response[date][a.data.status];
			response[date][a.data.status] = (x === undefined) ? 1 : x + 1;
		}
		if(a.data.payment_sum !== undefined)
			response[date].sum_paid += a.data.payment_sum;
		response[date].sum_total += a.price;
		response[date].total += 1;
	});
	return $.map(response, function(value, index) {
		value['date'] = index;
		return value;
	});
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
