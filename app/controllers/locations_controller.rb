class LocationsController < ApplicationController
  def index
    lang = params[:lang]
    start_date = stop_date = date = nil
    if params[:date]
      date = Time.parse(params[:date]).to_date
    elsif params[:start_date]
      start_date = Time.parse(params[:start_date]).to_date
      days = params[:days].to_i - 1
      stop_date = start_date + days
    end

    @locations = Location.order(:sort_order, lang == "en" ? "english_name" : "swedish_name")
      .where("sort_order IS NOT NULL")
    @locations.map.with_index { |loc,i| loc.sort_order = i }
    if start_date
      render json: { locations: @locations.as_json(lang: lang, start_date: start_date, stop_date: stop_date) }
    else
      render json: { locations: @locations.as_json(lang: lang, date: date) }
    end
  end
end
