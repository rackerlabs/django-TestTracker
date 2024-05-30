import { get_product_with_description_findings } from '../product/index.js';
var ObjFindings= {};
export var transferId = 0;
var productId = 0;
var productTypeId = 0;
var host = window.location.host;



$(document).on('click', '#id_transfer_finding_show_modal', function(event) {
    event.preventDefault();
    ObjFindings = {};
    transferId = $(this).data('transfer-id');
    productId = $(this).data('product-id');
    productTypeId = $(this).data('product-type-id');
    getTransferFindings(transferId)

    $(document).on('change', '.related-finding-chosen', function() {
        let selectedValue = $(this);
        let row = $(this).closest('tr');
        let finding = row.find('.btn-success');
        row.find('.cls-finding-status').text("Transfer Pending").css("color", "#333");
        let finding_id = finding.attr('data-btn-success');
        delete ObjFindings[finding_id];
        finding.attr('data-related-finding',selectedValue.val());
    });
});


$(document).ready(function() {

    $('#modalTransferFinding').on('click', '.btn-success, .btn-warning, .btn-danger', function() {
        let btnClass = $(this).attr('class');
        let row = $(this).closest('tr');
        if (btnClass.includes('btn-success')) {
            row.find('.cls-finding-status').text("Transfer Accepted").css("color", "green");
            let findingId = $(this).attr('data-btn-success');
            let relatedFinding = $(this).attr('data-related-finding');
            AcceptanceFinding(findingId, relatedFinding)
        } else if (btnClass.includes('btn-warning')) {
            row.find('.cls-finding-status').text("Transfer Rejected").css("color", "#e7a100");
            let findingId = $(this).attr('data-btn-warning');
            RejectFinding(findingId)
        } else if (btnClass.includes('btn-danger')) {
            row.find('.cls-finding-status').text("Transfer Removed").css("color", "red");
            let findingId = $(this).attr('data-btn-danger');
            RemoveFinding(findingId)
        }
        console.log(ObjFindings)
    }); 

});


export async function getTransferFindingsAsync(transferFindingId) {
    console.log("transfer-finding", transferFindingId)
    try {
        const response = await $.ajax({
            url: `/api/v2/transfer_finding?id=${transferFindingId}`,
            type: 'GET'
        });
        return response;
    } catch (error) {
        console.log(error);
        throw error;
    }
}
function AcceptanceFinding(findingId, related_finding){
    if(related_finding == ""){
        ObjFindings[findingId] = {"risk_status": "Transfer Accepted"}
    }
    else{
        ObjFindings[findingId] = {"risk_status": "Transfer Accepted", "related_finding": related_finding}
    }
    console.log(ObjFindings)
}
function RemoveFinding(findingId){
    ObjFindings[findingId] = {"risk_status": "Transfer Removed"}
}

function RejectFinding(findingId){
    ObjFindings[findingId] = {"risk_status": "Transfer Rejected"}
}

function requestRiskStatusFinding(findingId, riskStatus){
    ObjFindings[findingId] = {"risk_status": riskStatus}
}
Array.prototype.add = function(value){
    if (!this.includes(value)){
        this.push(value)
    }
    
}
Array.prototype.remove = function(value) {
    let index = this.indexOf(value);
    if (index !== -1) {
        this.splice(index, 1);
    }
};

function innerData(data, findings_related){
    let tableBody = document.getElementById("id_data_transfer_finding")
    tableBody.innerHTML = ""
    data.results.forEach(function(transfer_finding_item){
        transfer_finding_item.transfer_findings.forEach(function(findings){
            let row = document.createElement("tr") 
            let cell_status = document.createElement("td")
            cell_status.className = "cls-finding-status"

            row.innerHTML = `
            <td><a href="http://${host}/finding/${findings.findings.id}", class="table-link cls-finding-id" target="_blank" type="button">${findings.findings.id}</a></td>
            <td>${findings.findings.title}</td>
            <td>${findings.findings.severity}</td>
            <td>${findings.findings.cve}</td>`
            if(findings.findings.risk_status.includes("Transfer Accepted")){
                row.innerHTML += `<td><a href="http://${host}/finding/${findings.finding_related}" class="table-link" target="_blank" type="button"> ${findings.finding_related} </a></td>`
                cell_status.innerHTML= `<span style="color:green">${findings.findings.risk_status}</span>`
            }else if(findings.findings.risk_status.includes("Transfer Reject")){
                row.innerHTML += `${findings_related}`
                cell_status.innerHTML = `<span style="color:#e7a100">Transfer Rejected</span>`
            }else{
                row.innerHTML += `${findings_related}`
                cell_status.innerHTML = `${findings.findings.risk_status}`
            }
            row.appendChild(cell_status)
            row.innerHTML += `<td>
                ${transfer_finding_item.actions.includes(2801) && transfer_finding_item.actions.includes(2802)? 
                    `<button type="button" class="btn btn-success btn-sm" data-btn-success=${findings.findings.id} data-related-finding=""> 
                        <i class="fas fa-check"></i>
                     </button>
                     <button type="button" class="btn btn-warning btn-sm" data-btn-warning=${findings.findings.id}>
                        <i class="fas fa-times"></i>
                     </button>`
                     :'--'}
                ${transfer_finding_item.actions.includes(2803) ? 
                    `<button type="button" class="btn btn-danger btn-sm" data-btn-danger=${findings.findings.id}>
                        <i class="fas fa-trash-alt"></i>
                    </button>
                     `: ''}
            </td>`; 
            
            tableBody.appendChild(row);
            $(".form-control-chosen").chosen();
        });
    });
}


async function getTransferFindings(transferFindingId){
    try
    {
        let related_findings = ""
        const transferFindingResponse = await $.ajax({
            url: "/api/v2/transfer_finding?id=" + transferFindingId,
            type: "GET",
        });
        related_findings += `<td> <select class="form-control form-control-chosen related-finding-chosen" data-placeholder="Please select..."><option value=""> New Finding </option>`
        if (transferFindingResponse.results.length == 1)
            {
                const product = await get_product_with_description_findings(transferFindingResponse.results[0].destination_product);
                for(let engagement of product.engagements_list){
                    for(let finding of engagement.findings){
                        related_findings += `<option value="${finding.id}"> ${finding.id} - ${finding.title}</option>`
                    }
                }
                related_findings += `</select></td>`
                innerData(transferFindingResponse, related_findings)
            }
            else
            {
                throw new Error('A single value was expected for the transferFindingResponse variable', transferFindingResponse)
            }
    }
    catch(error){
        console.error(error); 
        throw error;
    }
    
}

export function filterForStatus(status){
    let ObjFindingsCopy = deepCopy(ObjFindings)
    for(let findingId in ObjFindingsCopy){
        if(!status.includes(ObjFindingsCopy[findingId].risk_status)){
            delete ObjFindingsCopy[findingId] 
        }
    }
    return ObjFindingsCopy
}

export async function generateRequestTransferFindingUpdate(transferFindingId, riskStatus) {
    try {
        let requestFindingStatus = {};

        const response = await getTransferFindingsAsync(transferFindingId);
        
        response.results.forEach(function(transferFindings) {
            transferFindings.transfer_findings.forEach(function(finding) {
                requestFindingStatus[finding.findings.id] = {"risk_status": riskStatus};
            });
        });

        return requestFindingStatus;
    } catch (error) {
        console.error(error);
        throw error;
    }
}


function deepCopy(objeto) {
    return JSON.parse(JSON.stringify(objeto));
}

