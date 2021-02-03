$(document).ready(function() {
    var textarea = $('#submit-text').children("textarea")[0];

    textarea.addEventListener("input", function(){
    var maxlength = 750;
    textarea.maxLength = maxlength;
    var currentLength = this.value.length;

    $('#textarea_feedback').html(currentLength + '/750 karakters');
	});

});
