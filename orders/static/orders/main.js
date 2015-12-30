$(function() {
	var columns  = [
        {field: 'order_id', title: 'Order ID'},
        {field: 'created_on', formatter: dateFormatter, title: 'Created on'},
        {field: 'domain', title: 'Domain'},
        {field: 'price', title: 'Price'},
        {field: 'data', formatter: dataFormatter('status'), title: 'Status'},
        {field: 'data', formatter: dataFormatter('payment_status'), title: 'Payment status'},
        {field: 'data', formatter: dataFormatter('utm1'), title: 'Utm_source'},
        {field: 'data', formatter: dataFormatter('utm2'), title: 'Utm_campaign'},
        {field: 'data', formatter: dataFormatter('utm3'), title: 'Utm_content'},
        {field: 'data', formatter: dataFormatter('utm4'), title: 'Utm_term'},
        {events: 'window.operateEvents', formatter: actionsFormatter, title: 'Actions'},
	];

    window.operateEvents = {
		'click .remove': function (e, value, row, index) {
			$order_list.bootstrapTable('removeByUniqueId', row.pk);
			e.preventDefault();
		}
	};

	var $order_list = $('#orderList').bootstrapTable({
		columns: columns,
		pageSize: 25,
		pageList: '[50, 100, 250, All]',
		showRefresh: true
    }).on('post-body.bs.table', function () {
		Intercooler.processNodes($('.action'));
	});

});

function actionsFormatter(row, value) {
	return '<a href="#" class="action remove" ic-delete-from="/api/orders/' + value.pk + '/">Delete</a>'
}

function dataFormatter(field) {
	return function(row, value) {
		return value['data'][field];
	}
}

function dateFormatter(row, value) {
	return moment().utcOffset(value).format('DD.MM.YY HH:MM');
}
