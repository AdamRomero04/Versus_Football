class Button {
    constructor(text, selectedStats) {
      this.text = text;
      this.element = document.createElement('button');
      this.element.classList.add('graphicButtons');
      this.element.innerText = this.text;
      this.clickCounter = 0;
      var self = this;
      this.element.addEventListener('click', function() {
        if(self.clickCounter % 2 == 0){
            self.element.style.background = 'linear-gradient(90deg, rgba(232,95,202,1) 0%, rgba(85,27,198,1) 100%)';
            self.element.style.backgroundColor = 'red';
            self.clickCounter++;
            console.log(self.clickCounter)
        }
        else if(self.clickCounter % 2 == 1){
            self.element.style.background = 'rgb(55, 9, 97)';
            self.element.style.backgroundColor = '';
            self.clickCounter++;
            console.log(self.clickCounter)
        }
      });
    }
  }
  var statList = document.getElementsByClassName('statLabel');
  var statArray = [];
  let selectedStats = [];
  let leftGraphic = [];
  let rightGraphic = [];
  
  for (let i = 0; i < statList.length; i++) {
    statArray.push(statList[i].innerText);
  }
  console.log(statArray);
  
  var container = document.getElementsByClassName('buttonContainer')[0];
  for (let i = 0; i < statArray.length; i++) {
    let statButton = new Button(statArray[i], selectedStats);
    container.appendChild(statButton.element);
  }

  const generate = document.getElementById('generate');
  generate.addEventListener('click', function() {
    generate.style.background = 'linear-gradient(90deg, rgba(85,27,198,1) 0%, rgba(232,95,202,1) 100%)';
    allButtons = document.getElementsByClassName('graphicButtons')
    for(const button of allButtons){
      if(button.style.backgroundColor === 'red'){
        selectedStats.push(button.innerHTML)
      }
    }
  console.log(selectedStats)
  let info = document.body.innerHTML;
  const parser = new DOMParser();
  const parsedHtml = parser.parseFromString(info, "text/html");

  for(let i = 0; i < 5; i++){
    let myDiv = parsedHtml.getElementById(selectedStats[i])
    let myChildren = myDiv.childNodes;
    leftGraphic.push(myChildren[1].innerText)
    rightGraphic.push(myChildren[3].innerText)
  }
  let graphic = parsedHtml.getElementById('stats')
  let graphicChildren = graphic.childNodes;
  counter = 0;
  console.log(graphicChildren)
  for(let i = 1; i < 20; i += 4){
    let graphicChildrenChildren = graphicChildren[i].childNodes;
    graphicChildrenChildren[1].innerHTML = leftGraphic[counter];
    graphicChildrenChildren[3].innerHTML = selectedStats[counter]
    graphicChildrenChildren[5].innerHTML = rightGraphic[counter];
    graphicChildrenChildren[1].innerText = leftGraphic[counter];
    graphicChildrenChildren[3].innerText = selectedStats[counter]
    graphicChildrenChildren[5].innerText = rightGraphic[counter];
    counter++;
  }
  let graphicTop = parsedHtml.getElementById('graphicPlayerTop');
  let graphicBottom = parsedHtml.getElementById('graphicPlayerBottom');
  let namesLeft = parsedHtml.getElementById('namesLeft');
  let namesRight = parsedHtml.getElementById('namesRight');

  graphicNamesLeft = [];
  graphicNamesRight = [];

  let graphicTopChildren = graphicTop.childNodes;
  let leftBox = graphicTopChildren[1].childNodes;
  let leftNameTop = leftBox[1];
  let leftNameBottom = leftBox[3];                            //left graphic box
  let leftPos = graphicTopChildren[3];

  let graphicBottomChildren = graphicBottom.childNodes;
  let rightBox = graphicBottomChildren[3].childNodes;
  let rightNameTop = rightBox[1];                             //right graphic box
  let rightNameBottom = rightBox[3];
  let rightPos = graphicBottomChildren[1];

  let leftFullInfo = parsedHtml.getElementById('namesLeft');
  let leftFullInfoChildren = leftFullInfo.childNodes;
  let leftFullName = leftFullInfoChildren[1].innerHTML;
  let leftFullPos = leftFullInfoChildren[5].innerHTML;        //left player info
  let leftSplitName = leftFullName.split(' ');
  let leftLowerName = leftSplitName[0];
  let leftRestName = leftFullName.substring(leftFullName.indexOf(' ') + 1);
  leftPos.innerHTML = leftFullPos;
  leftPos.innerText = leftFullPos;
  leftNameTop.innerHTML = leftLowerName;
  leftNameTop.innerText = leftLowerName;
  leftNameBottom.innerHTML = leftRestName.toUpperCase();
  leftNameBottom.innerText = leftRestName.toUpperCase();;

  let rightFullInfo = parsedHtml.getElementById('namesRight');
  let rightFullInfoChildren = rightFullInfo.childNodes;
  let rightFullName = rightFullInfoChildren[1].innerHTML;
  let rightFullPos = rightFullInfoChildren[5].innerHTML;        //left player info
  let rightSplitName = rightFullName.split(' ');
  let rightLowerName = rightSplitName[0];
  let rightRestName = rightFullName.substring(rightFullName.indexOf(' ') + 1);
  rightPos.innerHTML = rightFullPos;
  rightPos.innerText = rightFullPos;
  rightNameTop.innerHTML = rightRestName.toUpperCase();
  rightNameTop.innerText = rightRestName.toUpperCase();
  rightNameBottom.innerHTML = rightLowerName;
  rightNameBottom.innerText = rightLowerName;

  let graphicLeft = parsedHtml.getElementById('graphicLeft');
  let graphicLeftChildren = graphicLeft.childNodes;
  let graphicLeftChildrenPlayer = graphicLeftChildren[1];
  let graphicLeftChildrenBox = graphicLeftChildren[3].childNodes;
  let graphicLeftChildrenFlag = graphicLeftChildrenBox[1];
  let graphicLeftChildrenClub = graphicLeftChildrenBox[3];
  let playerImageCont = parsedHtml.getElementById('leftImages');
  let playerImageContChildren = playerImageCont.childNodes;
  let playerImgSrc = playerImageContChildren[1].getAttribute('src');
  let clubImgSrc = playerImageContChildren[3].getAttribute('src');
  let flagImgSrc = playerImageContChildren[5].getAttribute('src');

  graphicLeftChildrenPlayer.style.backgroundImage =  'url(' + playerImgSrc + ')';
  graphicLeftChildrenFlag.style.backgroundImage =  'url(' + flagImgSrc + ')';
  graphicLeftChildrenClub.src = clubImgSrc;

  let graphicRight = parsedHtml.getElementById('graphicRight');
  let graphicRightChildren = graphicRight.childNodes;
  let graphicRightChildrenPlayer = graphicRightChildren[3];
  let graphicRightChildrenBox = graphicRightChildren[1].childNodes;
  let graphicRightChildrenFlag = graphicRightChildrenBox[3];
  let graphicRightChildrenClub = graphicRightChildrenBox[1];
  let playerImageContBot = parsedHtml.getElementById('rightImages');
  let playerImageContChildrenBot = playerImageContBot.childNodes;
  let playerImgSrcBot = playerImageContChildrenBot[1].getAttribute('src');
  let clubImgSrcBot = playerImageContChildrenBot[3].getAttribute('src');
  let flagImgSrcBot = playerImageContChildrenBot[5].getAttribute('src');
  console.log(graphicRightChildren)

  graphicRightChildrenPlayer.style.backgroundImage =  'url(' + playerImgSrcBot + ')';
  graphicRightChildrenFlag.style.backgroundImage =  'url(' + flagImgSrcBot + ')';
  graphicRightChildrenClub.src = clubImgSrcBot;
  document.body.innerHTML = parsedHtml.documentElement.innerHTML
  let leftNumberStats = [];
  leftGraphic.forEach( ele => leftNumberStats.push(+ele))
  var rightNumberStats = [];
  rightGraphic.forEach( ele => rightNumberStats.push(+ele))
  chooseStat = ['firstStat', 'secondStat', 'thirdStat', 'fourthStat', 'fifthStat']
  let finish = 0;
  let barChartCount = 0;

  for(let i = 0; i < 5; i++){
  let bar1 = document.getElementById(chooseStat[i]).getContext('2d')
  let data2 = {
    labels: ['Left'], // Labels for the bars
    datasets: [{
      label: 'L',
      data: [leftNumberStats[i]], // Values for the bars
      backgroundColor: ['#ff6384'], // Fill colors for the bars
      barThickness: 13,
    },{
      label: 'R',
      data: [rightNumberStats[i]], // Values for the bars
      backgroundColor: ['#4426eb'], // Fill colors for the bars
      barThickness: 13,
    }]
  };

  var options = {
    indexAxis: 'y',
    scales: {
      x: {
        stacked: true,
        display: false, // Hide the x-axis
        maintainAspectRatio: true,
        max: leftNumberStats[i] + rightNumberStats[i],
      },
      y: {
        stacked: true,
        display: false, // Hide the y-axis
        maintainAspectRatio: true,
      }
    },
    plugins: {
      legend: {
        display: false // Hide the legend
      }
    },
    barPercentage: 1.0,
    categoryPercentage: 1.0,
    animation:{
      onComplete: function() {
        if(finish === 0 && barChartCount === 4){
        let target = document.getElementById('graphic');
  
        html2canvas(target, {
          letterRendering: 1,
          allowTaint: false,
          useCORS: true,  
        }).then(function(canvas) {
        var dataUrl = canvas.toDataURL();
        const downloadLink = document.createElement('a');
        downloadLink.href = dataUrl;
        downloadLink.download = 'my-chart.png';
        downloadLink.click();
        finish = 1;
        return;
        });
      }
      barChartCount++;
      }
    }
    };

  const barChart = new Chart(bar1, {
    type:'bar',
    data: data2,
    options: options
  });
  };
});


