class Location < ActiveRecord::Base
  def as_json(options = {})
    lang = options[:lang]
    date = options[:date]
    start_date = options[:start_date]
    stop_date = options[:stop_date]
    data = {
      id: id,
      swedish_name: swedish_name,
      english_name: english_name,
      sort_order: sort_order
    }

    if lang == "en"
      data[:name] = english_name
    else
      data[:name] = swedish_name
    end

    if date
      data[:openhour] = Openhour.get_single_day(id, date).as_json(embedded: true, lang: lang)
    end

    if start_date && stop_date
      data[:openhours] = Openhour.get_multiple_days(id, start_date, stop_date).as_json(embedded: true, lang: lang)
    end

    data
  end
end
