temp_json_path = '../../JSON/' + $("#objdata").attr('objname') + '.json';

$.getJSON(temp_json_path,function(data){
  $( "#RA" ).append( data.RA + "<br><br>" );
  $( "#DEC" ).append( data.DEC + "<br><br>");
  $( "#SOURCE" ).append( data.SOURCE + "<br><br>");
  $( "#PSPIN" ).append( data.PSPIN + "<br><br>");
  $( "#PORB" ).append( data.PORB + "<br><br>");
  $( "#M2" ).append( data.M2 + "<br><br>");
  $( "#D" ).append( data.D + "<br><br>");
  $( "#F" ).append( data.F + "<br><br>");
  $( "#AV" ).append( data.AV + "<br><br>");
  $( "#OPT" ).append( data.OPT + "<br><br>");
  $( "#YEAR" ).append( data.YEAR + "<br><br>");
  $( "#SURVEY" ).append( data.SURVEY + "<br><br>");
  $( "#TYPE" ).append( data.TYPE + "<br><br>");
  $( "#OBSERVED" ).append( data.OBSERVED + "<br><br>");
  $( "#COMPLETED" ).append( data.COMPLETED + "<br><br>");
  $( "#COMMENTS" ).append( data.COMMENTS + "<br><br>");
});
