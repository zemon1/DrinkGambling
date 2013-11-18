<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" xmlns:tal="http://xml.zope.org/namespaces/tal">
	<head>
		<link rel="stylesheet" type="text/css" href="../static/style.css">
		<!--<style>
			.card {
				background-image: url('../static/Cards/BlueBack.svg'); /*!important;*/
				background-size: 300%;
				width: 100px;
				height: 150px;
				background-position: center;
			}
		</style>--!>
		<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
		
		
		<script type="text/javascript">
			$(document).ready(function() {
				$("#deal").click(function() {
					$.ajax({
						type: "POST",
						url: "/deal",
						//data: {"contact_id": user_id},
						cache: false,
						success: function(result) {
							$('#deal').html("Dealt");
							//$('#deal').unbind('click');
							$('#cards').append(result['dealt'][0]);
							
							//If the player got black jack
							if(result['winner'] == -1){
								$('#shoe').html("Player has Blackjack");
							}

							$('#dealer .cardList').html('');
							$('#player .cardList').html('');
							
							for(var i = 1; i <= result['dealt'].length; i++) {
								var url = '../static/Cards/'+result['dealt'][i-1]+'.svg';
							
								if(i < 3){
									console.log("Loop " + i);
									$('#dealer .cardList').append('<li><div id="cd' + i + '" class="card" style="background-image:url(\'' + url + '\');"></div></li>');
								
								}else{
									console.log("Loop " + i);
									$('#player .cardList').append('<li><div id="cd' + i + '" class="card" style="background-image:url(\'' + url + '\');"></div></li>');

								}
							
								$('#dealer').append('</ul>');
								$('#player').append('</ul>');
							}
							console.log(result);
						}
					});
				});
			});
			$(document).ready(function() {
				$("#stand").click(function() {
					$.ajax({
						type: "POST",
						url: "/stand",
						cache: false,
						success: function(result) {
							$('#stand').html("Stood");
							//$('#stand').unbind('click');
							var winner = result['winner'];
							
							if(winner == 1){
								$('#shoe').html("Dealer Wins!<br>You'll get'em next time champ!");
							}else if (winner == -1){
								$('#shoe').html("You Won!<br>You should probably quit while you're ahead...");
							}else{
								$('#shoe').html("This round was a push, sorry bud.");
							}

							var dCards = result['dealerCards'];

							$('#dealer .cardList').html('');

							for(var i = 10; i-10 < dCards.length; i++){
								var url = '../static/Cards/' + dCards[i-10] + '.svg';
								

							//	setTimeout(function() {
								$('#dealer .cardList').append('<li><div id="cd' + i + '" class="card" style="background-image:url(\'' + url + '\');"></div></li>');
							//	}, 1000);
								
							}
							$('#dealer').append('</ul>');

							console.log(dCards);
						}
					});
				});
			});
			$(document).ready(function() {
				$("#hit").click(function() {
					$.ajax({
						type: "POST",
						url: "/hit",
						cache: false,
						success: function(result) {
							$('#hit').html("TapDat");
							//$('#hit').unbind('click');
							var pCards = result['playerCards'];
							var winner = result['winner'];

							if(winner == 1){
								$('#shoe').html('You Bust!  Dealer wins!')
							}

							$('#player .cardList').html('');
							
							for(var i = 20; i-20 < pCards.length; i++){
								var url = '../static/Cards/' + pCards[i-20] + '.svg';
								
								$('#player .cardList').append('<li><div id="cd' + i + '" class="card" style="background-image:url(\'' + url + '\');"></div></li>');
							}
							$('#player').append('</ul>');

							console.log(pCards);
						}
					});
				});
			});
		</script>
		
	
	</head>
	
	<body>
		<div id="shoe">
			${cards}
	 	</div>	
		
		<div class="buttons">
			<ul class="buttonList">
				<li>
					<button type="button" id="deal"> Deal </button>
				</li>
				<li>
					<button type="button" id="stand"> Stand </button>
				</li>
				<li>
					<button type="button" id="hit"> Hit </button>
				</li>
			</ul>
			<ul class="buttonList">
				<li>
					<button type="button" id="split"> Split </button>
				</li>
				<li>
					<button type="button" id="double"> Double </button>
				</li>
				<li>
					<button type="button" id="insurance"> Insurance </button>
				</li>
			</ul>
			<ul class="buttonList">
				<li>
					<button type="button" id="betUp"> Increase Bet </button>
				</li>
				<li>
					<button type="button" id="betDown"> Decrease Bet </button>
				</li>
				<li>
					<button type="button" id="surrender"> Surrender </button>
				</li>
			</ul>
		</div>
		
		<!-- Dealer --!>
		<div id="dealer">
			<ul class="cardList">

			</ul>
		</div>
		
		<!-- Player --!>
		<div id="player">
			<ul class="cardList">

			</ul>
		</div>
		
	</body>
</html>
