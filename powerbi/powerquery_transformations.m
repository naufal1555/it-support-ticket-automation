let
    // Power Query M Script for IT Support Tickets Ingestion & Transformation
    // Author: Ahmad Fathin Naufal (UGM) - System Developer
    Source = Csv.Document(File.Contents("data/processed/it_tickets_200.csv"),[Delimiter=",", Columns=16, Encoding=65001, QuoteStyle=QuoteStyle.Rtf]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"TicketID", type text},
        {"Title", type text},
        {"Category", type text},
        {"Priority", type text},
        {"SLAHours", Int64.Type},
        {"RequesterID", type text},
        {"RequesterName", type text},
        {"Department", type text},
        {"AssignedSpecialist", type text},
        {"Status", type text},
        {"CreatedDate", type datetime},
        {"DueDate", type datetime},
        {"ResolvedDate", type datetime},
        {"ResolutionTimeHours", type number},
        {"SLABreached", type logical},
        {"CSATScore", Int64.Type}
    }),
    #"Added SLA Performance Band" = Table.AddColumn(#"Changed Type", "PerformanceBand", each 
        if [SLABreached] = true then "Breached"
        else if [ResolutionTimeHours] <= ([SLAHours] * 0.5) then "Fast (<50% SLA)"
        else "Standard", type text
    )
in
    #"Added SLA Performance Band"
