<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" xmlns:tal="http://xml.zope.org/namespaces/tal">
	<head>
		<link rel="stylesheet" type="text/css" href="../static/style.css">
		<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
		
		<script type="text/javascript">
			$(document).ready(function() {
				//Initialize the page buttons
				setButtons();
			});

			$(document).ready(function() {
				$("#deal").click(function() {
					//Turn all the buttons off while the server is thinking
					disableAll();

					$.ajax({
						type: "POST",
						url: "/deal",
						//data: {"contact_id": user_id},
						cache: false,
						success: function(result) {
							setButtons(result);
							
							console.log("Deal");
							
							$('#shoe').html("");
							
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
					//Turn all the buttons off while the server is thinking
					disableAll();

					$.ajax({
						type: "POST",
						url: "/stand",
						cache: false,
						success: function(result) {
							setButtons(result);
							
							console.log("Stand");
							
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
				$("#split").click(function() {
					//Turn all the buttons off while the server is thinking
					disableAll();

					$.ajax({
						type: "POST",
						url: "/split",
						cache: false,
						success: function(result) {
							setButtons(result);
							
							$('#split').html("Split'd");

							console.log("Split");
						}
					});
				});
			});
			$(document).ready(function() {
				$("#hit").click(function() {
					//Turn all the buttons off while the server is thinking
					disableAll();

					$.ajax({
						type: "POST",
						url: "/hit",
						cache: false,
						success: function(result) {
							setButtons(result);
							
							console.log("Hit");
							
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

			$(document).ready(function() {
				$("#double").click(function() {
					//Turn all the buttons off while the server is thinking
					disableAll();

					$.ajax({
						type: "POST",
						url: "/double",
						cache: false,
						success: function(result) {
							setButtons(result);
							
							console.log("Double");
							
							$('#double').html("Dubbed");
							//$('#double').unbind('click');
							var pCards = result['playerCards'];
							var dCards = result['dealerCards'];
							var winner = result['winner'];


							$('#player .cardList').html('');
							
							for(var i = 20; i-20 < pCards.length; i++){
								var url = '../static/Cards/' + pCards[i-20] + '.svg';
								
								$('#player .cardList').append('<li><div id="cd' + i + '" class="card" style="background-image:url(\'' + url + '\');"></div></li>');
							}
							$('#player').append('</ul>');

							console.log(pCards);
							
							//Trigger the stand function
							if(winner == 1){
								$('#shoe').html('You Bust!  Dealer wins!')
								
								//Reveal dealer cards if the player bust
								$('#dealer .cardList').html('');
								
								for(var i = 10; i-10 < dCards.length; i++){
									var url = '../static/Cards/' + dCards[i-10] + '.svg';
									
									$('#dealer .cardList').append('<li><div id="cd' + i + '" class="card" style="background-image:url(\'' + url + '\');"></div></li>');
								}
								$('#dealer').append('</ul>');

							}else{
								$('#stand').trigger("click");
							}
						}
					});
				});
			});
			
			function setButtons(options){
				console.log("In");
				
				//Handle Buttons
				//Disable all first, then enable only allowed ones
				console.log("Disable all");
				$(":input").attr("disabled", true);
				if(!options){	
						$('#deal').removeAttr("disabled");
						$('#betUp').removeAttr("disabled");
						$('#betDown').removeAttr("disabled");
						$('#deal').html("Deal");
						$('#betUp').html("Increase Bet");
						$('#betDown').html("Decrease Bet");
					
				}else{
					if(options['canDeal'] == 1){
						console.log("cDeal");
						$('#deal').removeAttr("disabled");
						$('#deal').html("Deal");
					}
					
					if(options['canStand'] == 1){
						console.log("cStand");
						$('#stand').removeAttr("disabled");
						$('#stand').html("Stand");
					}

					if(options['canHit'] == 1){
						console.log("cHit");
						$('#hit').removeAttr("disabled");
						$('#hit').html("Hit");
					}

					if(options['canSplit'] == 1){
						console.log("cSplit");
						$('#split').removeAttr("disabled");
						$('#split').html("Split");
					}

					if(options['canDouble'] == 1){
						console.log("cDouble");
						$('#double').removeAttr("disabled");
						$('#double').html("Double");
					}

					if(options['canInsurance'] == 1){
						console.log("cInsurance");
						$('#insurance').removeAttr("disabled");
						$('#insurance').html("Insurance");
					}

					if(options['canSurrender'] == 1){
						console.log("cSurrender");
						$('#surrender').removeAttr("disabled");
						$('#surrender').html("Surrender");
					}

					if(options['canIncrease'] == 1){
						console.log("cIncrease");
						$('#betUp').removeAttr("disabled");
						$('#betUp').html("Increase Bet");
					}

					if(options['canDecrease'] == 1){
						console.log("cDecrease");
						$('#betDown').removeAttr("disabled");
						$('#betDown').html("Decrease Bet");
					}
				}
			}
			
			function disableAll(){
				$(":input").attr("disabled", true);
			}
		</script>
		
	
	</head>
	
	<body>
		<div id="shoe">
	 	</div>	
		
		<!-- Dealer --!>
		<div id="dealer">
			<b><p class="cardHeading"> Dealers Cards:</p></b>
			<ul class="cardList">

			</ul>
		</div>
		
		<!-- Player --!>
		<div id="player">
			<b><p class="cardHeading"> Players Cards:</p></b>
			<ul class="cardList">

			</ul>
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
	</body>
</html>
