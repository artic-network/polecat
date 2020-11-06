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
    <script src="https://cdn.jsdelivr.net/gh/rambaut/figtree.js@8f3ad96/dist/figtree.umd.js"></script>
    <script src="https://d3js.org/d3.v6.min.js"></script>

    <style>
    body {
      padding-top: 50px;
      font-family: "HelveticaNeue-Light", "Helvetica Neue Light", "Helvetica Neue", Helvetica, Arial, "Lucida Grande", sans-serif;
    }
    table text{
        font-family: "HelveticaNeue-Light", "Helvetica Neue Light", "Helvetica Neue", Helvetica, Arial, "Lucida Grande", sans-serif; 
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
    </style>

  </head>

  <body>

    </script>
    
    <script type="text/javascript">
        function buildTree(svgID, myTreeString) {
            const margins = {top:50,bottom:60,left:100,right:250}
            const svg = d3.select(document.getElementById(svgID))
            svg.selectAll("g").remove();

            const newickString = myTreeString;
            const tree = figtree.Tree.parseNewick(newickString);
            const fig = new figtree.FigTree(document.getElementById(svgID),margins, tree)
            fig.layout(figtree.rectangularLayout)
                          .nodes(figtree.circle()
                                  .attr("r",8)
                                  .hilightOnHover(20)
                                  .attr("stroke","dimgrey"),
                                figtree.tipLabel(v=>v.name)
                                  )
                          .nodeBackgrounds(figtree.circle()
                                            .attr("r", 10)
                                            .attr("fill","dimgrey")
                                            
                                            
                                          )
                          .branches(figtree.branch()
                                      .hilightOnHover(20)
                              )
        }
    </script>

    <div class="container">

      <div class="starter-template">
        <header>
            polecat | 
            <small class="text-muted">Phylogenetic Overview & Local Epidemiological Cluster Analysis Tool</small>
            <hr>
        </header>
        <h1>COG-UK Clusters
            <small class="text-muted">${date}</small>
        </h1>
        <br>
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
              <td>${row["cluster_no"]}</td>
              <td>${row["most_recent_tip"]}</td>
              <td>${row["tip_count"]}</td>
              <td>${row["admin0_count"]}</td>
              <td>${row["admin1_count"]}</td>
              <td>${row["admin2_count"]}</td>
            </tr>
        % endfor
        </table>

        
        % for cluster in cluster_data:
          <h2>Cluster ${cluster['cluster_no']}</h2>
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
        <svg width="600" height="400" id="tree_${cluster['cluster_no']}"></svg>
        <script type="text/javascript">
        buildTree("tree_${cluster['cluster_no']}", "${cluster['treeString']}");
        </script>

        % endfor

    <footer>
        <!-- <img src=https://raw.githubusercontent.com/COG-UK/polecat/master/docs/doc_figures/polecat_logo.svg vertical-align="middle" width="100" height="100" style="float:right;"></img> -->
        <hr>
        <p>
        <span style="float:left;">Rambaut Lab, University of Edinburgh, 2020<br><small class="text-muted">GNU General Public License v3.0</small></span>
        <span style="float:right;"> polecat ${version} | <small class="text-muted">Phylogenetic Overview & Local Epidemiological Cluster Analysis Tool</small> </span>

        <br><br>
        </p>

    </footer>
    </div>
    

    <script src="https://code.jquery.com/jquery-1.12.4.min.js" integrity="sha384-nvAa0+6Qg9clwYCGGPpDQLVpLNn0fRaROjHqs13t4Ggj3Ez50XnGQqc/r8MhnRDZ" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js" integrity="sha384-aJ21OjlMXNL5UyIl/XNwTMqvzeRMZH2w8c5cRVpzpU8Y5bApTppSuUkhZXN0VxHd" crossorigin="anonymous"></script>
  </body>
</html>
