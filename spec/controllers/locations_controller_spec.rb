require 'rails_helper'

RSpec.describe LocationsController, :type => :controller do
  before :each do
    setup_locations
    setup_openhours
  end
  describe "GET locations" do
    it "should return list of locations" do
      get :index
      expect(json).to have_key('locations')
    end

    it "should return list sorted by sort order and name" do
      get :index
      expect(json['locations'][0]['id']).to eq(2)
      expect(json['locations'][1]['id']).to eq(1)
      expect(json['locations'][2]['id']).to eq(3)
    end

    it "should sort by lang name if lang specified" do
      get :index, lang: 'sv'
      expect(json['locations'][0]['id']).to eq(2)
      expect(json['locations'][1]['id']).to eq(1)
      expect(json['locations'][2]['id']).to eq(3)
      get :index, lang: 'en'
      expect(json['locations'][0]['id']).to eq(1)
      expect(json['locations'][1]['id']).to eq(2)
      expect(json['locations'][2]['id']).to eq(3)
    end

    it "should set name to language name or swedish by default" do
      get :index
      expect(json['locations'][0]['name']).to eq("Plats 3")
      get :index, lang: 'en'
      expect(json['locations'][0]['name']).to eq("Location 1")
      get :index, lang: 'sv'
      expect(json['locations'][0]['name']).to eq("Plats 3")
    end

    it "should include openhour for single provided date in each location" do
      get :index, date: '2014-11-30'
      expect(json['locations'][0]).to have_key('openhour')
      expect(json['locations'][0]['openhour']).to_not have_key('location')
      expect(json['locations'][0]['openhour']['weekday']).to have_key('sv')
      expect(json['locations'][0]['openhour']['weekday']).to have_key('en')
    end

    it "should include openhour for range of provided dates in each location" do
      get :index, start_date: '2014-05-01', days: 7
      expect(json['locations'][0]).to have_key('openhours')
      expect(json['locations'][0]['openhours'][0]).to_not have_key('location')
      expect(json['locations'][0]['openhours'][0]['weekday']).to have_key('sv')
      expect(json['locations'][0]['openhours'][0]['weekday']).to have_key('en')
    end

    it "should include openhour for single provided date with single lang if lang provided" do
      get :index, date: '2014-05-01', lang: "sv"
      expect(json['locations'][0]).to have_key('openhour')
      expect(json['locations'][0]['openhour']['weekday']).to eq('Torsdag')
      get :index, date: '2014-05-01', lang: "en"
      expect(json['locations'][0]).to have_key('openhour')
      expect(json['locations'][0]['openhour']['weekday']).to eq('Thursday')
    end

    it "should include openhour for range provided dates with single lang if lang provided" do
      get :index, start_date: '2014-05-01', days: 7, lang: "sv"
      expect(json['locations'][0]).to have_key('openhours')
      expect(json['locations'][0]['openhours'][0]['weekday']).to eq('Torsdag')
      get :index, start_date: '2014-05-01', days: 7, lang: "en"
      expect(json['locations'][0]).to have_key('openhours')
      expect(json['locations'][0]['openhours'][0]['weekday']).to eq('Thursday')
    end

    it "should not return inactive locations" do
      get :index
      expect(json['locations'].count).to eq(3)
    end
  end
end
