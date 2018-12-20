<!DOCTYPE html>
<html>
   <head>
      <title>MedNet</title>

      <meta name="viewport" content="width=device-width,
        initial-scale=1">
     
     <link rel="stylesheet"
        href="https://www.w3schools.com/w3css/4/w3.css">

   </head>


   <style>
   th {
       text-align: left;

   }
   table {
      width: 100%;
   }

   body  {
      background-color: #CFE8EE;
   }

   .floatright {
      float: right;
    }

    .details {
      text-decoration: none;
      background-color: #87CEEB;
      color: #000;
      padding: 2px 6px 2px 6px;
      border-top: 1px solid #000;
      border-right: 1px solid #000;
      border-bottom: 1px solid #000;
      border-left: 1px solid #000;
      float: right;
    }

    .floatleft {
      float: left;
    }

   #biomarkers {
      width: 100%;
    }

    #biomarkers td, #biomarkers th {
      border: .5px solid #ddd;
      padding: 8px;
    }

    #biomarkers tr:nth-child(even){background-color: #f2f2f2;}
    #biomarkers tr:nth-child(odd){background-color: #cccccc;}

    #biomarkers th {
      padding-top: 12px;
      padding-bottom: 12px;
      text-align: left;
      background-color: #87CEEB;
      color: black;
  }

    .footer {
       position: fixed;
       left: 0;
       bottom: 0;
       width: 100%;
       text-align: center;
       background-color: #87CEEB;
    }

    .inputtable{
        table-layout: fixed;
        width: 100%;
    }

    .container {
      display: block;
      position: relative;
      padding-left: 35px;
      cursor: pointer;
      -webkit-user-select: none;
      -moz-user-select: none;
      -ms-user-select: none;
      user-select: none;
    }

    /* Hide the browser's default checkbox */
    .container input {
      position: absolute;
      opacity: 0;
      cursor: pointer;
      height: 0;
      width: 0;
    }

    /* Create a custom checkbox */
    .checkmark {
      position: absolute;
      top: 0;
      left: 0;
      height: 25px;
      width: 25px;
      background-color: #eee;
    }

    /* On mouse-over, add a grey background color */
    .container:hover input ~ .checkmark {
      background-color: #ccc;
    }

    /* When the checkbox is checked, add a blue background */
    .container input:checked ~ .checkmark {
      background-color: #87CEEB;
    }

    /* Create the checkmark/indicator (hidden when not checked) */
    .checkmark:after {
      content: "";
      position: absolute;
      display: none;
    }

    /* Show the checkmark when checked */
    .container input:checked ~ .checkmark:after {
      display: block;
    }

    /* Style the checkmark/indicator */
    .container .checkmark:after {
      left: 9px;
      top: 5px;
      width: 5px;
      height: 10px;
      border: solid black;
      border-width: 0 3px 3px 0;
      -webkit-transform: rotate(45deg);
      -ms-transform: rotate(45deg);
      transform: rotate(45deg);
    }

  
   </style>

   <body>

      <div class="w3-container w3-light-blue header">
         <center>
            <h1 style=font-size:200%><strong>MedNet</strong></h1>
            <h3>Automated Literature Summary Tool</h3>
         </center>
      </div>

      <br>

      <div class="w3-container">
        <form action="searchform" method="post">
          <center>

              <!-- <div class=floatleft>
                <input type="text" placeholder = "Disease" id="disease" name="disease" value='{{disease}}'>
              </div>
              <div class=floatright>
                <input type="submit" value="Submit">
              </div>
              <br><br> -->
              <table id = "inputtable">
              <colgroup>
                <col style="width: 18%" />
                <col style="width: 13%" />
                <col style="width: 12%" />
                <col style="width: 14%" />
                <col style="width: 17%" />
                <col style="width: 15.5%" />
                <col style="width: 11%" />
                <col style="width: auto" />
              </colgroup>
              <tr>
                <td><input type="text" placeholder = "Disease" id="disease" name="disease" value='{{disease}}' list="options"></td>
                <datalist id="options">
                % for option in disease_options:
                  <option value='{{option}}'>
                % end
                </datalist>
                % if diseases == True:
                  <td><label class="container">Diseases
                    <input type="checkbox" checked = "checked" name="diseases" value="diseases">
                    <span class="checkmark"></span>
                  </label></td>
                % else:
                  <td><label class="container">Diseases
                    <input type="checkbox" name="diseases" value="diseases">
                    <span class="checkmark"></span>
                  </label></td>
                % end
                % if genes == True:
                  <td><label class="container">Genes
                    <input type="checkbox" checked="checked" name="genes" value="genes">
                    <span class="checkmark"></span>
                  </label></td>
                % else:
                  <td><label class="container">Genes
                    <input type="checkbox" name="genes" value="genes">
                    <span class="checkmark"></span>
                  </label></td>
                % end
                % if chemicals == True:
                  <td><label class="container">Chemicals
                    <input type="checkbox" checked="checked" name="chemicals" value="chemicals">
                    <span class="checkmark"></span>
                  </label></td>
                % else:
                  <td><label class="container">Chemicals
                    <input type="checkbox" name="chemicals" value="chemicals">
                    <span class="checkmark"></span>
                  </label></td>
                % end
                % if pmutations == True:
                  <td><label class="container">Protein Mutations
                    <input type="checkbox" checked="checked" name="pmutations" value="pmutations">
                    <span class="checkmark"></span>
                  </label></td>
                % else:
                  <td><label class="container">Protein Mutations
                    <input type="checkbox" name="pmutations" value="pmutations">
                    <span class="checkmark"></span>
                  </label></td>
                % end
                % if dnamutations == True:
                  <td><label class="container">DNA Mutations
                    <input type="checkbox" checked="checked" name="dnamutations" value="dnamutations">
                    <span class="checkmark"></span>
                  </label></td>
                % else:
                  <td><label class="container">DNA Mutations
                    <input type="checkbox" name="dnamutations" value="dnamutations">
                    <span class="checkmark"></span>
                  </label></td>
                % end
                % if snps == True:
                  <td><label class="container">SNPs
                    <input type="checkbox" checked="checked" name="snps" value="snps">
                    <span class="checkmark"></span>
                  </label></td>
                % else:
                  <td><label class="container">SNPs
                    <input type="checkbox" name="snps" value="snps">
                    <span class="checkmark"></span>
                  </label></td>
                % end
                <td align = "right"><input type="submit" value="Submit"></td>
              </tr>
              </table>
          <center>
        </form>
      </div>

      <br>

      <!-- Form results -->
       <div class="w3-container" id = "biomarkers" style="overflow-x:auto;">
        <table >
          <tr>
            <th>Rank</th>
            <th>Biomarker</th> 
            <th>Type</th>
            <th>Relevant PubMed Journal Articles</th>
          </tr>

            % if len(top_results) != 0:
            %    i = 1
            %    for result in top_results:
                    <tr>
                      <td>{{i}}</td>
                      <td>{{result}}</td>
                      <td>{{top_result_types[i-1]}}</td>
                      <td>
                        % for article in top_result_articles_1[i-1]:
                            <a href="https://www.ncbi.nlm.nih.gov/pubmed/{{article}}" target="_blank">{{article}}</a>
                        % end
                        <a href="/details?marker={{result}}&disease={{disease}}" target="_blank" class="details">Show All Details</a>
                    </tr>
            %       i += 1
            %    end
            % end
            
       
        </table>

        % if len(top_results) == 0:
          No Results.
        % end
      </div>

      <br><br>
      <div class="footer">
      <font size="4">
        Created by Rebecca Barber.
      </font>
      </div>

   </body>

   
</html> 
