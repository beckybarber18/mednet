<!DOCTYPE html>
<html>
   <head>
      <title>MedNet Details</title>

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

    .floatleft {
      float: left;
    }

    .footer {
       position: fixed;
       left: 0;
       bottom: 0;
       width: 100%;
       text-align: center;
       background-color: #87CEEB;
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

  
   </style>

   <body>

      <div class="w3-container w3-light-blue header">
         <center>
            <h1 style=font-size:200%><strong>MedNet</strong></h1>
            <h3>PubMed Papers about <strong><u>{{disease}}</u></strong> and <strong><u>{{marker}}</u></strong></h3>
         </center>
      </div>

      <br>

      <div class="w3-container" id = "biomarkers" style="overflow-x:auto;">
        <table >
          <tr>
            <th>PubMed ID</th>
            <th>Title</th> 
            <th>Date</th>
          </tr>

            % if len(articles) != 0:
            %   i = 0
            %   for article in articles:
                  <tr>
                    <td><a href="https://www.ncbi.nlm.nih.gov/pubmed/{{article}}" target="_blank">{{article}}</a></td>
                    % if titles[i] == '':
                      <td>'Not Found'</td>
                    % else:
                      <td>{{titles[i]}}</td>
                    % end
                    % if dates[i] == 0:
                      <td>'Not Found'</td>
                    % else:
                      <td>{{dates[i]}}</td>
                    % end
                  </tr>
            %     i += 1
            %   end
            % end
        </table>

        % if len(articles) == 0:
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
