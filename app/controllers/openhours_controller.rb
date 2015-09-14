class OpenhoursController < ApplicationController
  def index
    location_id = params[:location_id]
    start_date = Time.parse(params[:start_date]).to_date if params[:start_date]
    multiple_dates = false
    if start_date
      multiple_dates = true
    end
    if multiple_dates
      days = params[:days].to_i - 1
      stop_date = start_date + days
      @openhours = Openhour.get_multiple_days(location_id, start_date, stop_date)
      render json: {openhours: @openhours}
    else
      date = params[:date] ? Time.parse(params[:date]) :  Time.now
      date = date.to_date
      @openhour = Openhour.get_single_day(location_id, date)
      render json: {openhour: @openhour}
    end
  end
end
