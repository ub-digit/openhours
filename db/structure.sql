--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

--
-- Name: plpgsql; Type: PROCEDURAL LANGUAGE; Schema: -; Owner: -
--

CREATE PROCEDURAL LANGUAGE plpgsql;


SET search_path = public, pg_catalog;

--
-- Name: plpgsql_call_handler(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION plpgsql_call_handler() RETURNS language_handler
    LANGUAGE c
    AS '$libdir/plpgsql', 'plpgsql_call_handler';


SET default_tablespace = '';

SET default_with_oids = true;

--
-- Name: bokning; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE bokning (
    obj_id integer NOT NULL,
    typ integer NOT NULL,
    dag date,
    start numeric(4,2) NOT NULL,
    slut numeric(4,2) NOT NULL,
    bokad boolean DEFAULT false,
    bokad_barcode character varying(14),
    status integer DEFAULT 1,
    kommentar character varying(100)
);


--
-- Name: bokning_backup; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE bokning_backup (
    obj_id integer NOT NULL,
    typ integer NOT NULL,
    dag date,
    start numeric(4,2) NOT NULL,
    slut numeric(4,2) NOT NULL,
    bokad boolean DEFAULT false,
    bokad_barcode character varying(14),
    status integer DEFAULT 1,
    kommentar character varying(100)
);


--
-- Name: boknings_objekt; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE boknings_objekt (
    obj_id integer NOT NULL,
    typ integer NOT NULL,
    lokal_id integer NOT NULL,
    namn character varying(100) NOT NULL,
    plats character varying(30) NOT NULL,
    ska_kvitteras boolean,
    kommentar character varying(200),
    aktiv boolean DEFAULT true,
    intern_bruk boolean DEFAULT false
);


--
-- Name: typ_1_grupprum; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE typ_1_grupprum (
    obj_id integer NOT NULL,
    antal_platser numeric(3,0),
    finns_dator boolean,
    finns_tavla boolean,
    kommentar character varying(200)
);


--
-- Name: booking_objects; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW booking_objects AS
    SELECT bo.obj_id AS id, bo.typ AS object_type, bo.lokal_id AS location_id, bo.namn AS name, bo.plats AS place, bo.ska_kvitteras AS require_confirmation, bo.kommentar AS comment, bo.aktiv AS active, bo.intern_bruk AS internal, t.antal_platser AS seats, t.finns_dator AS has_computer, t.finns_tavla AS has_whiteboard FROM (boknings_objekt bo JOIN typ_1_grupprum t ON ((t.obj_id = bo.obj_id)));


--
-- Name: bookings; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW bookings AS
    SELECT bokning.oid AS id, bokning.obj_id AS booking_object_id, bokning.dag AS pass_day, bokning.start AS pass_start, bokning.slut AS pass_stop, bokning.bokad AS booked, bokning.bokad_barcode AS booked_by, bokning.status, bokning.kommentar AS display_name FROM bokning;


--
-- Name: dag_ordning; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE dag_ordning (
    day character(10),
    ordning numeric(1,0),
    dag character(20)
);


--
-- Name: dagar; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE dagar (
    dag character varying(10),
    ordning numeric(1,0)
);


--
-- Name: gamla_bokningar; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE gamla_bokningar (
    obj_id integer NOT NULL,
    typ integer NOT NULL,
    dag date,
    start numeric(4,2) NOT NULL,
    slut numeric(4,2) NOT NULL,
    bokad boolean DEFAULT false,
    bokad_barcode character varying(14),
    status integer DEFAULT 1,
    kommentar character varying(100)
);


--
-- Name: gamla_openhours; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE gamla_openhours (
    lokal_id integer NOT NULL,
    day character(10) NOT NULL,
    open numeric(4,2) NOT NULL,
    close numeric(4,2) NOT NULL,
    prioritet numeric(1,0) DEFAULT 2 NOT NULL,
    from_dag date,
    nummer numeric(1,0)
);


--
-- Name: lokal; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE lokal (
    id integer NOT NULL,
    namn character varying(100) NOT NULL,
    name text
);


--
-- Name: lokal_sort; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE lokal_sort (
    id integer,
    sort_order integer
);


--
-- Name: locations; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW locations AS
    SELECT l.id, l.name AS english_name, l.namn AS swedish_name, ls.sort_order FROM (lokal l JOIN lokal_sort ls ON ((l.id = ls.id)));


--
-- Name: obj_id; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE obj_id
    START WITH 1
    INCREMENT BY 1
    MAXVALUE 99999
    NO MINVALUE
    CACHE 1;


--
-- Name: openhours; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE openhours (
    lokal_id integer NOT NULL,
    day character(10) NOT NULL,
    open numeric(4,2) NOT NULL,
    close numeric(4,2) NOT NULL,
    prioritet numeric(1,0) DEFAULT 2 NOT NULL,
    from_dag date
);


--
-- Name: pga_diagrams; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE pga_diagrams (
    diagramname character varying(64) NOT NULL,
    diagramtables text,
    diagramlinks text
);


--
-- Name: pga_forms; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE pga_forms (
    formname character varying(64) NOT NULL,
    formsource text
);


--
-- Name: pga_graphs; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE pga_graphs (
    graphname character varying(64) NOT NULL,
    graphsource text,
    graphcode text
);


--
-- Name: pga_images; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE pga_images (
    imagename character varying(64) NOT NULL,
    imagesource text
);


--
-- Name: pga_layout; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE pga_layout (
    tablename character varying(64) NOT NULL,
    nrcols smallint,
    colnames text,
    colwidth text
);


--
-- Name: pga_queries; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE pga_queries (
    queryname character varying(64) NOT NULL,
    querytype character(1),
    querycommand text,
    querytables text,
    querylinks text,
    queryresults text,
    querycomments text
);


--
-- Name: pga_reports; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE pga_reports (
    reportname character varying(64) NOT NULL,
    reportsource text,
    reportbody text,
    reportprocs text,
    reportoptions text
);


--
-- Name: pga_scripts; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE pga_scripts (
    scriptname character varying(64) NOT NULL,
    scriptsource text
);


--
-- Name: typ_info; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE typ_info (
    typ integer,
    typ_namn character varying(100),
    timmar_pass integer,
    antal_pass integer,
    dagar_fram integer,
    typ_namn_stor character varying(100),
    from_dag date,
    type_name text,
    type_name_heading text
);


--
-- Name: stat2; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW stat2 AS
    SELECT b.dag, b.start, b.slut, b.status, bo.namn AS objekt, bo.lokal_id AS bib, l.namn AS bibliotek, t.typ_namn AS typ FROM (((gamla_bokningar b JOIN boknings_objekt bo ON ((b.obj_id = bo.obj_id))) JOIN lokal l ON ((bo.lokal_id = l.id))) JOIN typ_info t ON ((t.typ = b.typ))) WHERE ((b.dag >= '2006-01-01'::date) AND (b.dag <= '2006-12-31'::date));


--
-- Name: stat_2006; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW stat_2006 AS
    SELECT b.dag, b.start, b.slut, b.status, bo.namn AS objekt, l.namn AS bibliotek, t.typ_namn AS typ FROM (((gamla_bokningar b JOIN boknings_objekt bo ON ((b.obj_id = bo.obj_id))) JOIN lokal l ON ((bo.lokal_id = l.id))) JOIN typ_info t ON ((t.typ = b.typ))) WHERE ((b.dag >= '2006-01-01'::date) AND (b.dag <= '2006-12-31'::date));


--
-- Name: typ_2_datorer; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE typ_2_datorer (
    obj_id integer NOT NULL,
    webb boolean,
    ordbehandling boolean,
    skrivare boolean,
    kommentar character varying(200),
    extra_tangentbord integer,
    diskettstation integer DEFAULT 1
);


--
-- Name: typ_3_lasstudio; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE typ_3_lasstudio (
    obj_id integer,
    braille boolean,
    kommentar character varying(200)
);


--
-- Name: pga_diagrams_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY pga_diagrams
    ADD CONSTRAINT pga_diagrams_pkey PRIMARY KEY (diagramname);


--
-- Name: pga_forms_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY pga_forms
    ADD CONSTRAINT pga_forms_pkey PRIMARY KEY (formname);


--
-- Name: pga_graphs_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY pga_graphs
    ADD CONSTRAINT pga_graphs_pkey PRIMARY KEY (graphname);


--
-- Name: pga_images_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY pga_images
    ADD CONSTRAINT pga_images_pkey PRIMARY KEY (imagename);


--
-- Name: pga_layout_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY pga_layout
    ADD CONSTRAINT pga_layout_pkey PRIMARY KEY (tablename);


--
-- Name: pga_queries_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY pga_queries
    ADD CONSTRAINT pga_queries_pkey PRIMARY KEY (queryname);


--
-- Name: pga_reports_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY pga_reports
    ADD CONSTRAINT pga_reports_pkey PRIMARY KEY (reportname);


--
-- Name: pga_scripts_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY pga_scripts
    ADD CONSTRAINT pga_scripts_pkey PRIMARY KEY (scriptname);


--
-- Name: typ_3_lasstudio_obj_id_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY typ_3_lasstudio
    ADD CONSTRAINT typ_3_lasstudio_obj_id_key UNIQUE (obj_id);


--
-- Name: boknings_objekt_obj_id_key; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE UNIQUE INDEX boknings_objekt_obj_id_key ON boknings_objekt USING btree (obj_id);


--
-- Name: typ_1_grupprum_obj_id_key; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE UNIQUE INDEX typ_1_grupprum_obj_id_key ON typ_1_grupprum USING btree (obj_id);


--
-- Name: typ_2_datorer_obj_id_key; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE UNIQUE INDEX typ_2_datorer_obj_id_key ON typ_2_datorer USING btree (obj_id);


--
-- PostgreSQL database dump complete
--

SET search_path TO "$user",public;

