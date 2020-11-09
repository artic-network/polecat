<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="https://raw.githubusercontent.com/COG-UK/polecat/master/docs/doc_figures/polecat_logo.svg">

    <title>polecat report</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-1.12.4.min.js" integrity="sha384-nvAa0+6Qg9clwYCGGPpDQLVpLNn0fRaROjHqs13t4Ggj3Ez50XnGQqc/r8MhnRDZ" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js" integrity="sha384-aJ21OjlMXNL5UyIl/XNwTMqvzeRMZH2w8c5cRVpzpU8Y5bApTppSuUkhZXN0VxHd" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/gh/rambaut/figtree.js@e03decdb/dist/figtree.umd.js"></script>
    <script src="https://d3js.org/d3.v6.min.js"></script>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <style>
    body {
      padding-top: 50px;
      font-family: "ArialNova-Light","HelveticaNeue-Light", "Helvetica Neue Light", "Helvetica Neue", Helvetica, Arial, "Lucida Grande", sans-serif;
    }
    table text{
        font-family: "ArialNova-Light","HelveticaNeue-Light", "Helvetica Neue Light", "Helvetica Neue", Helvetica, Arial, "Lucida Grande", sans-serif; 
    }
    header {
        display: block;
        text-align: right;
    
    }
    .center {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 50%;
        }
    .nodeBackgrounds{
        fill:dimgrey;
        stroke:dimgrey;
    }
    .node circle{
      stroke-width:0;
      cursor:pointer;
      fill:#86b0a6;
      stroke:dimgrey;
      }
    .svg-tooltip {
        background: rgba(69,77,93,.9);
        border-radius: .1rem;
        color: #fff;
        display: block;
        font-size: 14px;
        max-width: 320px;
        padding: .2rem .4rem;
        position: absolute;
        text-overflow: ellipsis;
        white-space: pre;
        z-index: 300;
        visibility: hidden;
  }
    .branch path{
    stroke-width:2;
    stroke: dimgrey;
    }
    .branch.hovered path{
      stroke-width:4;
      stroke: 4d4d4d;
    }
      .node.hovered circle{
      stroke-width:5;
      stroke: dimgrey
      }
      .node text{
         font-family: "HelveticaNeue-Light", "Helvetica Neue Light", "Helvetica Neue", Helvetica, Arial, "Lucida Grande", sans-serif; 
         font-weight: 300;
      }
    .starter-template {
      padding: 40px 15px;
      text-align: left;
    }
    .svg-icon {
    display: inline-flex;
    align-self: center;
    }
    h3{
        font-size: 1em;
    }
    #toTopBtn {
    position: fixed;
    bottom: 26px;
    right: 39px;
    z-index: 98;
    padding: 21px;
    background-color: #86b0a6
    }
    .js .cd-top--fade-out {
        opacity: .5
    }
    .js .cd-top--is-visible {
        visibility: visible;
        opacity: 1
    }

    .js .cd-top {
        visibility: hidden;
        opacity: 0;
        transition: opacity .3s, visibility .3s, background-color .3s
    }

    .cd-top {
        position: fixed;
        bottom: 20px;
        bottom: var(--cd-back-to-top-margin);
        right: 20px;
        right: var(--cd-back-to-top-margin);
        display: inline-block;
        height: 40px;
        height: var(--cd-back-to-top-size);
        width: 40px;
        width: var(--cd-back-to-top-size);
        box-shadow: 0 0 10px rgba(0, 0, 0, .05) !important;
        background: url(https://res.cloudinary.com/dxfq3iotg/image/upload/v1571057658/cd-top-arrow.svg) no-repeat center 50%;
        background-color:#86b0a6;
        background-color: hsla(var(--cd-color-3-h), var(--cd-color-3-s), var(--cd-color-3-l), 0.8)
    }

    </style>

  </head>

  <body>
    <script>
      $(document).ready(function() {
        $(window).scroll(function() {
        if ($(this).scrollTop() > 20) {
        $('#toTopBtn').fadeIn();
        } else {
        $('#toTopBtn').fadeOut();
        }
        });
        
        $('#toTopBtn').click(function() {
        $("html, body").animate({
        scrollTop: 0
        }, 400);
        return false;
        });
        });
      </script>


    <script type="text/javascript">
      const updateTableFactory = (tooltipId,metadata)=>(tipId)=>{
              const data = metadata[tipId];
              const tableDiv = d3.select(document.getElementById(tooltipId));
              //Remove table
          tableDiv.html("")
              if (data !== undefined) {
                  const visibleData = Object.keys(data).filter(d=>d!=='sequence_name');
                  tableDiv.append("h3")
                      .attr("class",'tooltip-header')
                      .text(tipId);
                  tableDiv.selectAll("p")
                          .data(visibleData)
                          .enter()
                          .append("p")
                          .attr("class","tooltip-text")
                              .selectAll("span")
                              .data(d=>[d,data[d]])
                              .enter()
                              .append("span")
                              .attr("class",(d,i)=> i===0? "tooltip-key" :"tooltip-value")
                              .text((d,i)=>i===0?`${d} : `:d)
              }
      }
      function buildTree(svgID, myTreeString,tooltipID,backgroundDataString) {
          const backgroundData = JSON.parse(backgroundDataString);
          const updateTable = updateTableFactory(tooltipID, backgroundData);
          const margins = {top:50,bottom:60,left:100,right:250}
          const svg = d3.select(document.getElementById(svgID))
          svg.selectAll("g").remove();
          const newickString = myTreeString;
          const tree = figtree.Tree.parseNewick(newickString);
          const fig = new figtree.FigTree(document.getElementById(svgID),margins, tree)
          fig.layout(figtree.rectangularLayout)
                        .nodes(figtree.circle()
                                  .filter(n=>!n.children||n[fig.id].collapsed)
                                .attr("r",8)
                                .hilightOnHover(20)
                                .onClick(node=>updateTable(node.name)),
                              figtree.tipLabel(v=>v.name)
                                )
                        .nodeBackgrounds(figtree.circle()
                                          .attr("r", 10)
                                .filter(n=>!n.children||n[fig.id].collapsed)
                                        .attr("fill","dimgrey")
                                        )
                        .branches(figtree.branch()
                                    .hilightOnHover(20) 
                                    .collapseOnClick()
                            )
      }
    </script>

    <div class="container">
      <a href="#" id="toTopBtn" class="cd-top text-replace js-cd-top cd-top--is-visible cd-top--fade-out" data-abc="true"></a>
      <div class="page-header">
        <header>
            polecat | 
            <small class="text-muted">Phylogenetic Overview & Local Epidemiological Cluster Analysis Tool</small>
            <hr>
        </header>
        <h1>COG-UK Clusters
            <small class="text-muted">${date}</small>
        </h1>
        <br>
        </div>
        <p>        
        <strong>Command</strong>
        <pre> ${command} </pre>
        </p>
        <!-- <p class="lead">polecat identified 5 clusters</p> -->
    
    <br>

    <h3><strong>Table 1</strong> | Summary of clusters   <input style = "float:right" type="text" id="myInput" onkeyup="myFunction('myInput','myTable')" placeholder="Search for cluster..." title="searchbar"></h3>
    
    <table class="table table-striped" id="myTable">
        <tr class="header">
        <th style="width:10%;">Cluster number</th>
        <th style="width:10%">Most recent tip</th>
        <th style="width:10%;">Tip Count</th>
        <th style="width:10%;">Admin0 Count</th>
        <th style="width:10%;">Admin1 Count</th>
        <th style="width:10%;">Admin1 Count</th>
        </tr>
        % for row in summary_data:
            <tr>
              <td><a href="#${row['cluster_no']}" style="color:#86b0a6">${row["cluster_no"]}</a></td>
              <td>${row["most_recent_tip"]}</td>
              <td>${row["tip_count"]}</td>
              <td>${row["admin0_count"]}</td>
              <td>${row["admin1_count"]}</td>
              <td>${row["admin2_count"]}</td>
            </tr>
        % endfor
        </table>

        
        % for cluster in cluster_data:
          <h2><a id = "${cluster['cluster_no']}"></a>Cluster ${cluster['cluster_no']}</h2>
          <h3><strong>Table ${cluster['table_no']}</strong> | Cluster ${cluster['cluster_no']}</h3>
          <table class="table table-striped">
              <tr class="header">
              <th style="width:30%;">Statistic</th>
              <th style="width:60%;">Information</th>
              </tr>
              % for stat in cluster['stats']:
                <tr>
                  <td>${stat["statistic"]}</td>
                  <td>${stat["information"]}</td>
                </tr>
              % endfor
            </table>

        <br>
        <div class="row">
    
          <div class="col-xs-8">
            <svg width="600" height="400" id="tree_${cluster['cluster_no']}"></svg>
            </div>
            <div class="col-xs-4" id="tooltip_${cluster['cluster_no']}">
          </div>
          <script type="text/javascript">
            buildTree("tree_${cluster['cluster_no']}", "${cluster['treeString']}","tooltip_${cluster['cluster_no']}",'${background_data}');
            </script>
        </div>
        

        % endfor

        <script>
          function myFunction(myInput, myTable) {
            var input, filter, table, tr, td, i, txtValue;
            input = document.getElementById(myInput);
            filter = input.value.toUpperCase();
            table = document.getElementById(myTable);
            tr = table.getElementsByTagName("tr");
            for (i = 0; i < tr.length; i++) {
              td = tr[i].getElementsByTagName("td")[0];
              if (td) {
                txtValue = td.textContent || td.innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                  tr[i].style.display = "";
                } else {
                  tr[i].style.display = "none";
                }
              }       
            }
          }
          </script>
    <footer class="page-footer">
      <div class="container-fluid text-right text-md-right">
        <hr>
        <div class="row">
          <div class="col-sm-1">
            <p>
            <img src=https://raw.githubusercontent.com/COG-UK/polecat/master/docs/doc_figures/polecat_logo.svg vertical-align="left" width="50" height="50"></img>
            <p>
        </div>

      <div class="col-sm-11" style="text-align: right;">
        polecat ${version} | <small class="text-muted">Phylogenetic Overview & Local Epidemiological Cluster Analysis Tool</small> <br><small class="text-muted">GNU General Public License v3.0</small></div>

        <br><br>
        </p>
      </div>
    </footer>
    </div>
    

    <script src="https://code.jquery.com/jquery-1.12.4.min.js" integrity="sha384-nvAa0+6Qg9clwYCGGPpDQLVpLNn0fRaROjHqs13t4Ggj3Ez50XnGQqc/r8MhnRDZ" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js" integrity="sha384-aJ21OjlMXNL5UyIl/XNwTMqvzeRMZH2w8c5cRVpzpU8Y5bApTppSuUkhZXN0VxHd" crossorigin="anonymous"></script>
  </body>
</html>
