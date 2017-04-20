console.log("LOADED: base_main.js");
requirejs.config({
	paths: {
		jQuery: '/static/bower_components/jquery/dist/jquery.min',
		bootstrap: '/static/bower_components/bootstrap/dist/js/bootstrap.min',
		bootstrapDatepicker: 'https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/1.4.1/js/bootstrap-datepicker.min',
		underscore: '/static/bower_components/underscore/underscore-min',
		react: '/static/bower_components/react/react',
		reactDom: '/static/bower_components/react/react-dom',
	},
	"shim": {
		"bootstrap": ["jQuery"],
		"bootstrapDatepicker": ["jQuery", "bootstrap"]
	}
});

define([], function() {
});
