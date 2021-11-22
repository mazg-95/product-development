#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)
library(dplyr)
library(ggplot2)
library(DT)

# Define UI for application that draws a histogram
ui <- fluidPage(

    # Application title
    titlePanel("Shiny Plots"),

    fluidRow(column(6, plotOutput('plot', click='clk',
                                  dblclick = 'dclk',
                                  hover = 'mouse_hover',
                                  brush = 'mouse_brush')), 
             column(6, DT::dataTableOutput('mtcars_tbl'))),
    
    fluidRow(verbatimTextOutput('click_data'))
)

# Define server logic required to draw a histogram
server <- function(input, output, session) {

    output$plot <- renderPlot({
        mtcars %>% ggplot(aes(x=wt, y=mpg)) +
            geom_point(color='black', size=4) +
            ylab('MPG') +
            xlab('WT') +
            ggtitle('WT vs MPG')
    })
    
    output$mtcars_tbl <- DT::renderDataTable({
        mtcars
    })
    

    observeEvent(input$clk, {
        df <- nearPoints(mtcars, input$clk)
        output$plot <- renderPlot({
            mtcars %>% ggplot(aes(x=wt, y=mpg)) +
                geom_point(color='green', size=4) +
                ylab('MPG') +
                xlab('WT') +
                ggtitle('WT vs MPG')
        })
        
        output$mtcars_tbl <- DT::renderDataTable({
            df
        })
    })
    
    observeEvent(input$mouse_hover, {
        output$plot <- renderPlot({
            mtcars %>% ggplot(aes(x=wt, y=mpg)) +
                geom_point(color='gray', size=4) +
                ylab('MPG') +
                xlab('WT') +
                ggtitle('WT vs MPG')
        })
    })
    
    observeEvent(input$dclk, {
        output$plot <- renderPlot({
            mtcars %>% ggplot(aes(x=wt, y=mpg)) +
                geom_point(color='black', size=4) +
                ylab('MPG') +
                xlab('WT') +
                ggtitle('WT vs MPG')
        })
    })
    
    observeEvent(input$mouse_brush, {
        df <- brushedPoints(mtcars, input$mouse_brush, allRows = TRUE)
        highlight_df <- df %>% filter(selected_)
        df <- df %>% filter(!selected_)
        output$plot <- renderPlot({
            df  %>%  
                ggplot(aes(x=wt, y=mpg)) +
                geom_point(size=4, color='black') +
                geom_point(data=highlight_df,size=4, color='green') +
                ylab('MPG') +
                xlab('WT') +
                ggtitle('WT vs MPG')})
           
        
        output$mtcars_tbl <- DT::renderDataTable({
            highlight_df %>% select(-c(selected_))
        })
    })
}

# Run the application 
shinyApp(ui = ui, server = server)
