$(document).ready(function () {
    $("#upload_form").submit(function (e) {
      e.preventDefault();
      var formData = new FormData(this);
  
      $.ajax({
        url: "/upload_pdf",
        method: "POST",
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
          if (response.result === "success") {
            $("#document-id").val(response.document_id);
            alert("PDF uploaded successfully.");
  
            // Call pollForResult after the PDF is uploaded
            const documentId = $("#document-id").val();
            const option = $("#option").val();
            pollForResult(documentId, option);
          } else {
            alert("Error occurred. Please try again.");
          }
        },
        error: function () {
          alert("Error occurred. Please try again.");
        },
      });
    });
  });
  
  function showKeywords(data) {
    var keywordsContainer = $("#keywords");
  
    if (keywordsContainer.length === 0) {
      // Create the element if it doesn't exist
      keywordsContainer = $("<ul>").attr("id", "keywords");
      $("#upload_status").append(keywordsContainer);
    } else {
      // Empty the container if it exists
      keywordsContainer.empty();
    }
  
    if (data && data.length > 0) {
      data.forEach(function (keyword) {
        var keywordElement = $("<li>").text(keyword);
        keywordsContainer.append(keywordElement);
      });
    } else {
      keywordsContainer.append($("<li>").text("No keywords found."));
    }
  }
  function showSummary(data) {
    var summaryContainer = $("#summary");
  
    if (summaryContainer.length === 0) {
      // Create the element if it doesn't exist
      summaryContainer = $("<p>").attr("id", "summary");
      $("#results").append(summaryContainer);
    } else {
      // Empty the container if it exists
      summaryContainer.empty();
    }
  
    if (data) {
      summaryContainer.text(data);
    } else {
      summaryContainer.text("No summary available.");
    }
  }
  
  function pollForResult(documentId, option) {
    setTimeout(function () {
      $.ajax({
        url: "/get_result",
        method: "POST",
        data: { document_id: documentId, option: option },
        success: function (response) {
          if (response.error === 'Analysis is still in progress. Please try again later.') {
            console.log("Polling for result...");
            pollForResult(documentId, option);
          } else if (response.error) {
            alert(response.error);
          } else {
            if (option === "keywords") {
              showKeywords(response.result);
            } else if (option === "summary") {
              showSummary(response.result);
            }
          }
        },
        error: function () {
          alert("Error occurred. Please try again.");
        },
      });
    }, 2000); // Poll every 2 seconds
  }