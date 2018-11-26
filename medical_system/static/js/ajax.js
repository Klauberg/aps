$(function(){
    $('#cadastrar').click(function(event){
        event.preventDefault();
        link = this.href;
        $('#paciente').load(link);
    });
    $('#cadastrar-visita').click(function(event){
        event.preventDefault();
        link = this.href;
        $('#visitas').load(link);
    });
});
