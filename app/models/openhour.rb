# -*- coding: utf-8 -*-
class Openhour < ActiveRecord::Base
  WEEKDAYS=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
  SV_WEEKDAYS=["Måndag", "Tisdag", "Onsdag", "Torsdag", "Fredag", "Lördag", "Söndag"]
  belongs_to :location, class_name: "Location", foreign_key: 'lokal_id', primary_key: 'id'
  attr_accessor :date

  def self.get_single_day(location_id, day)
    single_day = get_priority_day(location_id, day).first
    if single_day.blank?
      single_day = get_weekday_day(location_id, day).first
    end
    if single_day.blank?
      single_day = get_closed_day(location_id, day)
    end
    single_day.date = day
    single_day
  end

  def self.get_multiple_days(location_id, start_date, stop_date)
    (start_date..stop_date).to_a.map do |day|
      get_single_day(location_id, day)
    end
  end

  def self.get_weekday_day(location_id, day)
    wday = WEEKDAYS[day.wday-1]
    Openhour.where(lokal_id: location_id).where(day: wday)
      .where("from_dag < ?", datestring(day))
      .order(:from_dag).reverse_order
  end

  def self.get_priority_day(location_id, day)
    Openhour.where(lokal_id: location_id).where(day: datestring(day)).where(prioritet: 1)
  end

  def self.get_closed_day(location_id, day)
    wday = WEEKDAYS[day.wday-1]
    from_date = Time.parse("1970-01-01").to_date
    Openhour.new(lokal_id: location_id, day: wday, prioritet: 2, open: 9, close: 9, from_dag: from_date)
  end

  def self.datestring(date)
    date.strftime("%Y-%m-%d")
  end

  def timestring(time)
    Time.parse(sprintf("%2.2f", time).gsub(/\./,':')).strftime("%H:%M")
  end

  def timestamp(day, time)
    Time.parse("#{day} #{timestring(time)}")
  end

  def string
    if open == close
      return {sv: "Stängt", en: "Closed"}
    end
    return {
      sv: "#{timestring(open)} - #{timestring(close)}",
      en: "#{timestring(open)} - #{timestring(close)}"
    }
  end

  def swedish_weekday
    weekday = WEEKDAYS.index(day.strip)
    if !weekday
      weekday = Time.parse(day).wday-1
    end
    SV_WEEKDAYS[weekday]
  end

  def english_weekday
    weekday = WEEKDAYS.index(day.strip)
    if !weekday
      weekday = Time.parse(day).wday-1
    end
    WEEKDAYS[weekday]
  end

  def as_json(options = {})
    embedded = options[:embedded]
    lang = options[:lang]

    data = {
      open: timestring(open),
      close: timestring(close),
      date: self.date,
      location: {
        sv: location.swedish_name,
        en: location.english_name
      },
      weekday: {
        sv: swedish_weekday,
        en: english_weekday
      },
      string: string,
      timestamps: {
        open: timestamp(self.date, open),
        close: timestamp(self.date, close)
      },
      is_exception: prioritet == 1,
      is_open: (open != close)
    }

    if embedded
      data.delete(:location)
    end

    if lang
      data[:weekday] = data[:weekday][lang.to_sym] || swedish_weekday
      data[:string] = data[:string][lang.to_sym] || string[:sv]
    end

    data
  end
end
