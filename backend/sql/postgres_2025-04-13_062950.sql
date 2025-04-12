--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4 (ServBay)
-- Dumped by pg_dump version 17.4 (ServBay)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: system_config; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.system_config (
    id integer NOT NULL,
    title character varying(100) NOT NULL,
    favicon character varying(500) NOT NULL,
    logo character varying(500) NOT NULL,
    background character varying(500) NOT NULL,
    copyright character varying(500) NOT NULL,
    keep_record character varying(500) NOT NULL,
    help_url character varying(500) NOT NULL,
    privacy_url character varying(500) NOT NULL,
    clause_url character varying(500) NOT NULL,
    code_url character varying(500) NOT NULL,
    description text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    creator_id integer
);


ALTER TABLE public.system_config OWNER TO tao;

--
-- Name: TABLE system_config; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.system_config IS '配置表';


--
-- Name: COLUMN system_config.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_config.id IS '主键ID';


--
-- Name: COLUMN system_config.title; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_config.title IS '网站标题';


--
-- Name: COLUMN system_config.favicon; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_config.favicon IS '网站favicon';


--
-- Name: COLUMN system_config.logo; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_config.logo IS '网站logo';


--
-- Name: COLUMN system_config.background; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_config.background IS '网站背景';


--
-- Name: COLUMN system_config.copyright; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_config.copyright IS '版权信息';


--
-- Name: COLUMN system_config.keep_record; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_config.keep_record IS '备案信息';


--
-- Name: COLUMN system_config.help_url; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_config.help_url IS '帮助链接';


--
-- Name: COLUMN system_config.privacy_url; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_config.privacy_url IS '隐私政策链接';


--
-- Name: COLUMN system_config.clause_url; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_config.clause_url IS '服务条款链接';


--
-- Name: COLUMN system_config.code_url; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_config.code_url IS '源码地址';


--
-- Name: COLUMN system_config.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_config.description IS '备注说明';


--
-- Name: COLUMN system_config.created_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_config.created_at IS '创建时间';


--
-- Name: COLUMN system_config.updated_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_config.updated_at IS '更新时间';


--
-- Name: COLUMN system_config.creator_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_config.creator_id IS '创建人ID';


--
-- Name: system_config_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.system_config_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.system_config_id_seq OWNER TO tao;

--
-- Name: system_config_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.system_config_id_seq OWNED BY public.system_config.id;


--
-- Name: system_dept; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.system_dept (
    id integer NOT NULL,
    name character varying(40) NOT NULL,
    "order" integer NOT NULL,
    parent_id integer,
    available boolean NOT NULL,
    description text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.system_dept OWNER TO tao;

--
-- Name: TABLE system_dept; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.system_dept IS '部门表';


--
-- Name: COLUMN system_dept.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dept.id IS '主键ID';


--
-- Name: COLUMN system_dept.name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dept.name IS '部门名称';


--
-- Name: COLUMN system_dept."order"; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dept."order" IS '显示排序';


--
-- Name: COLUMN system_dept.parent_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dept.parent_id IS '父级部门ID';


--
-- Name: COLUMN system_dept.available; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dept.available IS '是否启用(True:启用 False:禁用)';


--
-- Name: COLUMN system_dept.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dept.description IS '备注说明';


--
-- Name: COLUMN system_dept.created_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dept.created_at IS '创建时间';


--
-- Name: COLUMN system_dept.updated_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dept.updated_at IS '更新时间';


--
-- Name: system_dept_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.system_dept_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.system_dept_id_seq OWNER TO tao;

--
-- Name: system_dept_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.system_dept_id_seq OWNED BY public.system_dept.id;


--
-- Name: system_dict_data; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.system_dict_data (
    id integer NOT NULL,
    dict_sort integer,
    dict_label character varying(100),
    dict_value character varying(100),
    dict_type character varying(100),
    css_class character varying(100),
    list_class character varying(100),
    is_default boolean,
    available boolean,
    description text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    creator_id integer
);


ALTER TABLE public.system_dict_data OWNER TO tao;

--
-- Name: TABLE system_dict_data; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.system_dict_data IS '数据字典数据表';


--
-- Name: COLUMN system_dict_data.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_data.id IS '字典编码';


--
-- Name: COLUMN system_dict_data.dict_sort; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_data.dict_sort IS '字典排序';


--
-- Name: COLUMN system_dict_data.dict_label; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_data.dict_label IS '字典标签';


--
-- Name: COLUMN system_dict_data.dict_value; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_data.dict_value IS '字典键值';


--
-- Name: COLUMN system_dict_data.dict_type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_data.dict_type IS '字典类型';


--
-- Name: COLUMN system_dict_data.css_class; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_data.css_class IS '样式属性（其他样式扩展）';


--
-- Name: COLUMN system_dict_data.list_class; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_data.list_class IS '表格回显样式';


--
-- Name: COLUMN system_dict_data.is_default; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_data.is_default IS '是否默认（Y是 N否）';


--
-- Name: COLUMN system_dict_data.available; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_data.available IS '状态（0正常 1停用）';


--
-- Name: COLUMN system_dict_data.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_data.description IS '备注说明';


--
-- Name: COLUMN system_dict_data.created_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_data.created_at IS '创建时间';


--
-- Name: COLUMN system_dict_data.updated_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_data.updated_at IS '更新时间';


--
-- Name: COLUMN system_dict_data.creator_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_data.creator_id IS '创建人ID';


--
-- Name: system_dict_data_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.system_dict_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.system_dict_data_id_seq OWNER TO tao;

--
-- Name: system_dict_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.system_dict_data_id_seq OWNED BY public.system_dict_data.id;


--
-- Name: system_dict_type; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.system_dict_type (
    id integer NOT NULL,
    dict_name character varying(100),
    dict_type character varying(100),
    available boolean,
    description text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    creator_id integer
);


ALTER TABLE public.system_dict_type OWNER TO tao;

--
-- Name: TABLE system_dict_type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.system_dict_type IS '数据字典类型表';


--
-- Name: COLUMN system_dict_type.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_type.id IS '字典主键';


--
-- Name: COLUMN system_dict_type.dict_name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_type.dict_name IS '字典名称';


--
-- Name: COLUMN system_dict_type.dict_type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_type.dict_type IS '字典类型';


--
-- Name: COLUMN system_dict_type.available; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_type.available IS '状态（0正常 1停用）';


--
-- Name: COLUMN system_dict_type.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_type.description IS '备注说明';


--
-- Name: COLUMN system_dict_type.created_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_type.created_at IS '创建时间';


--
-- Name: COLUMN system_dict_type.updated_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_type.updated_at IS '更新时间';


--
-- Name: COLUMN system_dict_type.creator_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_dict_type.creator_id IS '创建人ID';


--
-- Name: system_dict_type_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.system_dict_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.system_dict_type_id_seq OWNER TO tao;

--
-- Name: system_dict_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.system_dict_type_id_seq OWNED BY public.system_dict_type.id;


--
-- Name: system_job; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.system_job (
    id integer NOT NULL,
    name character varying(64),
    jobstore character varying(64),
    executor character varying(64),
    trigger character varying(64) NOT NULL,
    trigger_args text,
    func text NOT NULL,
    args text,
    kwargs text,
    "coalesce" boolean,
    max_instances integer,
    start_date text,
    end_date text,
    status boolean,
    message character varying(500),
    description text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    creator_id integer
);


ALTER TABLE public.system_job OWNER TO tao;

--
-- Name: TABLE system_job; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.system_job IS '定时任务调度表';


--
-- Name: COLUMN system_job.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_job.id IS '任务ID';


--
-- Name: COLUMN system_job.name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_job.name IS '任务名称';


--
-- Name: COLUMN system_job.jobstore; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_job.jobstore IS '存储器';


--
-- Name: COLUMN system_job.executor; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_job.executor IS '执行器:将运行此作业的执行程序的名称';


--
-- Name: COLUMN system_job.trigger; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_job.trigger IS '触发器:控制此作业计划的 trigger 对象';


--
-- Name: COLUMN system_job.trigger_args; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_job.trigger_args IS '触发器参数';


--
-- Name: COLUMN system_job.func; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_job.func IS '任务函数';


--
-- Name: COLUMN system_job.args; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_job.args IS '位置参数';


--
-- Name: COLUMN system_job.kwargs; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_job.kwargs IS '关键字参数';


--
-- Name: COLUMN system_job."coalesce"; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_job."coalesce" IS '是否合并运行:是否在多个运行时间到期时仅运行作业一次';


--
-- Name: COLUMN system_job.max_instances; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_job.max_instances IS '最大实例数:允许的最大并发执行实例数 工作';


--
-- Name: COLUMN system_job.start_date; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_job.start_date IS '开始时间';


--
-- Name: COLUMN system_job.end_date; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_job.end_date IS '结束时间';


--
-- Name: COLUMN system_job.status; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_job.status IS '任务状态:正常,停止';


--
-- Name: COLUMN system_job.message; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_job.message IS '日志信息';


--
-- Name: COLUMN system_job.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_job.description IS '备注说明';


--
-- Name: COLUMN system_job.created_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_job.created_at IS '创建时间';


--
-- Name: COLUMN system_job.updated_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_job.updated_at IS '更新时间';


--
-- Name: COLUMN system_job.creator_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_job.creator_id IS '创建人ID';


--
-- Name: system_job_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.system_job_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.system_job_id_seq OWNER TO tao;

--
-- Name: system_job_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.system_job_id_seq OWNED BY public.system_job.id;


--
-- Name: system_menu; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.system_menu (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    type integer NOT NULL,
    "order" integer NOT NULL,
    permission character varying(100),
    available boolean NOT NULL,
    icon character varying(50),
    route_name character varying(100),
    route_path character varying(200),
    component_path character varying(200),
    redirect character varying(200),
    hidden boolean NOT NULL,
    cache boolean NOT NULL,
    parent_id integer,
    description text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.system_menu OWNER TO tao;

--
-- Name: TABLE system_menu; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.system_menu IS '菜单表';


--
-- Name: COLUMN system_menu.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_menu.id IS '主键ID';


--
-- Name: COLUMN system_menu.name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_menu.name IS '菜单名称';


--
-- Name: COLUMN system_menu.type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_menu.type IS '菜单类型';


--
-- Name: COLUMN system_menu."order"; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_menu."order" IS '显示排序';


--
-- Name: COLUMN system_menu.permission; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_menu.permission IS '权限标识(如：system:user:list)';


--
-- Name: COLUMN system_menu.available; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_menu.available IS '是否启用(True:启用 False:禁用)';


--
-- Name: COLUMN system_menu.icon; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_menu.icon IS '菜单图标';


--
-- Name: COLUMN system_menu.route_name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_menu.route_name IS '路由名称';


--
-- Name: COLUMN system_menu.route_path; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_menu.route_path IS '路由路径';


--
-- Name: COLUMN system_menu.component_path; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_menu.component_path IS '组件路径';


--
-- Name: COLUMN system_menu.redirect; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_menu.redirect IS '重定向地址';


--
-- Name: COLUMN system_menu.hidden; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_menu.hidden IS '是否隐藏(True:隐藏 False:显示)';


--
-- Name: COLUMN system_menu.cache; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_menu.cache IS '是否缓存(True:是 False:否)';


--
-- Name: COLUMN system_menu.parent_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_menu.parent_id IS '父级菜单ID';


--
-- Name: COLUMN system_menu.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_menu.description IS '备注说明';


--
-- Name: COLUMN system_menu.created_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_menu.created_at IS '创建时间';


--
-- Name: COLUMN system_menu.updated_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_menu.updated_at IS '更新时间';


--
-- Name: system_menu_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.system_menu_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.system_menu_id_seq OWNER TO tao;

--
-- Name: system_menu_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.system_menu_id_seq OWNED BY public.system_menu.id;


--
-- Name: system_notice; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.system_notice (
    id integer NOT NULL,
    notice_title character varying(50) NOT NULL,
    notice_type integer NOT NULL,
    notice_content text,
    available boolean NOT NULL,
    description text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    creator_id integer
);


ALTER TABLE public.system_notice OWNER TO tao;

--
-- Name: TABLE system_notice; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.system_notice IS '通知公告表';


--
-- Name: COLUMN system_notice.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_notice.id IS '主键ID';


--
-- Name: COLUMN system_notice.notice_title; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_notice.notice_title IS '公告标题';


--
-- Name: COLUMN system_notice.notice_type; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_notice.notice_type IS '公告类型（1通知 2公告）';


--
-- Name: COLUMN system_notice.notice_content; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_notice.notice_content IS '公告内容';


--
-- Name: COLUMN system_notice.available; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_notice.available IS '是否启用(True:启用 False:禁用)';


--
-- Name: COLUMN system_notice.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_notice.description IS '备注说明';


--
-- Name: COLUMN system_notice.created_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_notice.created_at IS '创建时间';


--
-- Name: COLUMN system_notice.updated_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_notice.updated_at IS '更新时间';


--
-- Name: COLUMN system_notice.creator_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_notice.creator_id IS '创建人ID';


--
-- Name: system_notice_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.system_notice_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.system_notice_id_seq OWNER TO tao;

--
-- Name: system_notice_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.system_notice_id_seq OWNED BY public.system_notice.id;


--
-- Name: system_operation_log; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.system_operation_log (
    id integer NOT NULL,
    request_path character varying(255),
    request_method character varying(10),
    request_payload text,
    request_ip character varying(50),
    request_os character varying(64),
    request_browser character varying(64),
    response_code integer,
    response_json text,
    description text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    creator_id integer
);


ALTER TABLE public.system_operation_log OWNER TO tao;

--
-- Name: TABLE system_operation_log; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.system_operation_log IS '操作日志表';


--
-- Name: COLUMN system_operation_log.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_operation_log.id IS '主键ID';


--
-- Name: COLUMN system_operation_log.request_path; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_operation_log.request_path IS '请求路径';


--
-- Name: COLUMN system_operation_log.request_method; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_operation_log.request_method IS '请求方式';


--
-- Name: COLUMN system_operation_log.request_payload; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_operation_log.request_payload IS '请求体';


--
-- Name: COLUMN system_operation_log.request_ip; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_operation_log.request_ip IS '请求IP地址';


--
-- Name: COLUMN system_operation_log.request_os; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_operation_log.request_os IS '操作系统';


--
-- Name: COLUMN system_operation_log.request_browser; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_operation_log.request_browser IS '浏览器';


--
-- Name: COLUMN system_operation_log.response_code; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_operation_log.response_code IS '响应状态码';


--
-- Name: COLUMN system_operation_log.response_json; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_operation_log.response_json IS '响应体';


--
-- Name: COLUMN system_operation_log.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_operation_log.description IS '备注说明';


--
-- Name: COLUMN system_operation_log.created_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_operation_log.created_at IS '创建时间';


--
-- Name: COLUMN system_operation_log.updated_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_operation_log.updated_at IS '更新时间';


--
-- Name: COLUMN system_operation_log.creator_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_operation_log.creator_id IS '创建人ID';


--
-- Name: system_operation_log_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.system_operation_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.system_operation_log_id_seq OWNER TO tao;

--
-- Name: system_operation_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.system_operation_log_id_seq OWNED BY public.system_operation_log.id;


--
-- Name: system_position; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.system_position (
    id integer NOT NULL,
    name character varying(40) NOT NULL,
    "order" integer NOT NULL,
    available boolean NOT NULL,
    description text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    creator_id integer
);


ALTER TABLE public.system_position OWNER TO tao;

--
-- Name: TABLE system_position; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.system_position IS '岗位表';


--
-- Name: COLUMN system_position.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_position.id IS '主键ID';


--
-- Name: COLUMN system_position.name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_position.name IS '岗位名称';


--
-- Name: COLUMN system_position."order"; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_position."order" IS '显示排序';


--
-- Name: COLUMN system_position.available; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_position.available IS '是否启用(True:启用 False:禁用)';


--
-- Name: COLUMN system_position.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_position.description IS '备注说明';


--
-- Name: COLUMN system_position.created_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_position.created_at IS '创建时间';


--
-- Name: COLUMN system_position.updated_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_position.updated_at IS '更新时间';


--
-- Name: COLUMN system_position.creator_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_position.creator_id IS '创建人ID';


--
-- Name: system_position_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.system_position_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.system_position_id_seq OWNER TO tao;

--
-- Name: system_position_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.system_position_id_seq OWNED BY public.system_position.id;


--
-- Name: system_role; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.system_role (
    id integer NOT NULL,
    name character varying(40) NOT NULL,
    "order" integer NOT NULL,
    data_scope integer NOT NULL,
    available boolean NOT NULL,
    description text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    creator_id integer
);


ALTER TABLE public.system_role OWNER TO tao;

--
-- Name: TABLE system_role; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.system_role IS '角色表';


--
-- Name: COLUMN system_role.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_role.id IS '主键ID';


--
-- Name: COLUMN system_role.name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_role.name IS '角色名称';


--
-- Name: COLUMN system_role."order"; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_role."order" IS '显示排序';


--
-- Name: COLUMN system_role.data_scope; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_role.data_scope IS '数据权限范围';


--
-- Name: COLUMN system_role.available; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_role.available IS '是否启用(True:启用 False:禁用)';


--
-- Name: COLUMN system_role.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_role.description IS '备注说明';


--
-- Name: COLUMN system_role.created_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_role.created_at IS '创建时间';


--
-- Name: COLUMN system_role.updated_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_role.updated_at IS '更新时间';


--
-- Name: COLUMN system_role.creator_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_role.creator_id IS '创建人ID';


--
-- Name: system_role_depts; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.system_role_depts (
    role_id integer NOT NULL,
    dept_id integer NOT NULL
);


ALTER TABLE public.system_role_depts OWNER TO tao;

--
-- Name: TABLE system_role_depts; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.system_role_depts IS '角色部门关联表';


--
-- Name: COLUMN system_role_depts.role_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_role_depts.role_id IS '角色ID';


--
-- Name: COLUMN system_role_depts.dept_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_role_depts.dept_id IS '部门ID';


--
-- Name: system_role_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.system_role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.system_role_id_seq OWNER TO tao;

--
-- Name: system_role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.system_role_id_seq OWNED BY public.system_role.id;


--
-- Name: system_role_menus; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.system_role_menus (
    role_id integer NOT NULL,
    menu_id integer NOT NULL
);


ALTER TABLE public.system_role_menus OWNER TO tao;

--
-- Name: TABLE system_role_menus; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.system_role_menus IS '角色菜单关联表';


--
-- Name: COLUMN system_role_menus.role_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_role_menus.role_id IS '角色ID';


--
-- Name: COLUMN system_role_menus.menu_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_role_menus.menu_id IS '菜单ID';


--
-- Name: system_user_positions; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.system_user_positions (
    user_id integer NOT NULL,
    position_id integer NOT NULL
);


ALTER TABLE public.system_user_positions OWNER TO tao;

--
-- Name: TABLE system_user_positions; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.system_user_positions IS '用户岗位关联表';


--
-- Name: COLUMN system_user_positions.user_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_user_positions.user_id IS '用户ID';


--
-- Name: COLUMN system_user_positions.position_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_user_positions.position_id IS '岗位ID';


--
-- Name: system_user_roles; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.system_user_roles (
    user_id integer NOT NULL,
    role_id integer NOT NULL
);


ALTER TABLE public.system_user_roles OWNER TO tao;

--
-- Name: TABLE system_user_roles; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.system_user_roles IS '用户角色关联表';


--
-- Name: COLUMN system_user_roles.user_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_user_roles.user_id IS '用户ID';


--
-- Name: COLUMN system_user_roles.role_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_user_roles.role_id IS '角色ID';


--
-- Name: system_users; Type: TABLE; Schema: public; Owner: tao
--

CREATE TABLE public.system_users (
    id integer NOT NULL,
    username character varying(150) NOT NULL,
    password character varying(128) NOT NULL,
    name character varying(40) NOT NULL,
    mobile character varying(20),
    email character varying(255),
    gender integer NOT NULL,
    avatar character varying(255),
    available boolean NOT NULL,
    is_superuser boolean NOT NULL,
    last_login timestamp without time zone,
    dept_id integer,
    description text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    creator_id integer
);


ALTER TABLE public.system_users OWNER TO tao;

--
-- Name: TABLE system_users; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON TABLE public.system_users IS '用户表';


--
-- Name: COLUMN system_users.id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_users.id IS '主键ID';


--
-- Name: COLUMN system_users.username; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_users.username IS '用户名/登录账号';


--
-- Name: COLUMN system_users.password; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_users.password IS '密码';


--
-- Name: COLUMN system_users.name; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_users.name IS '姓名';


--
-- Name: COLUMN system_users.mobile; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_users.mobile IS '手机号';


--
-- Name: COLUMN system_users.email; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_users.email IS '邮箱';


--
-- Name: COLUMN system_users.gender; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_users.gender IS '性别(1:男 2:女 3:未知)';


--
-- Name: COLUMN system_users.avatar; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_users.avatar IS '头像地址';


--
-- Name: COLUMN system_users.available; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_users.available IS '是否启用(True:启用 False:禁用)';


--
-- Name: COLUMN system_users.is_superuser; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_users.is_superuser IS '是否为超级管理员';


--
-- Name: COLUMN system_users.last_login; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_users.last_login IS '最后登录时间';


--
-- Name: COLUMN system_users.dept_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_users.dept_id IS '部门ID';


--
-- Name: COLUMN system_users.description; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_users.description IS '备注说明';


--
-- Name: COLUMN system_users.created_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_users.created_at IS '创建时间';


--
-- Name: COLUMN system_users.updated_at; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_users.updated_at IS '更新时间';


--
-- Name: COLUMN system_users.creator_id; Type: COMMENT; Schema: public; Owner: tao
--

COMMENT ON COLUMN public.system_users.creator_id IS '创建人ID';


--
-- Name: system_users_id_seq; Type: SEQUENCE; Schema: public; Owner: tao
--

CREATE SEQUENCE public.system_users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.system_users_id_seq OWNER TO tao;

--
-- Name: system_users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tao
--

ALTER SEQUENCE public.system_users_id_seq OWNED BY public.system_users.id;


--
-- Name: system_config id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_config ALTER COLUMN id SET DEFAULT nextval('public.system_config_id_seq'::regclass);


--
-- Name: system_dept id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_dept ALTER COLUMN id SET DEFAULT nextval('public.system_dept_id_seq'::regclass);


--
-- Name: system_dict_data id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_dict_data ALTER COLUMN id SET DEFAULT nextval('public.system_dict_data_id_seq'::regclass);


--
-- Name: system_dict_type id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_dict_type ALTER COLUMN id SET DEFAULT nextval('public.system_dict_type_id_seq'::regclass);


--
-- Name: system_job id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_job ALTER COLUMN id SET DEFAULT nextval('public.system_job_id_seq'::regclass);


--
-- Name: system_menu id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_menu ALTER COLUMN id SET DEFAULT nextval('public.system_menu_id_seq'::regclass);


--
-- Name: system_notice id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_notice ALTER COLUMN id SET DEFAULT nextval('public.system_notice_id_seq'::regclass);


--
-- Name: system_operation_log id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_operation_log ALTER COLUMN id SET DEFAULT nextval('public.system_operation_log_id_seq'::regclass);


--
-- Name: system_position id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_position ALTER COLUMN id SET DEFAULT nextval('public.system_position_id_seq'::regclass);


--
-- Name: system_role id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_role ALTER COLUMN id SET DEFAULT nextval('public.system_role_id_seq'::regclass);


--
-- Name: system_users id; Type: DEFAULT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_users ALTER COLUMN id SET DEFAULT nextval('public.system_users_id_seq'::regclass);


--
-- Data for Name: system_config; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.system_config (id, title, favicon, logo, background, copyright, keep_record, help_url, privacy_url, clause_url, code_url, description, created_at, updated_at, creator_id) FROM stdin;
1	FastAPI Vue Admin	http://localhost:8000/api/v1/static/image/favicon.ico	http://localhost:8000/api/v1/static/image/logo.png	http://localhost:8000/api/v1/static/image/background.png	Copyright © 2021-2025 fastapi-vue-admin.com 版权所有	晋ICP备18005113号-3	https://gitee.com/tao__tao/fastapi_vue3_admin.git	https://gitee.com/tao__tao/fastapi_vue3_admin/blob/master/LICENSE	https://gitee.com/tao__tao/fastapi_vue3_admin/blob/master/LICENSE	https://gitee.com/tao__tao/fastapi_vue3_admin.git	FastAPI Vue Admin 是完全开源的权限管理系统	2025-04-13 06:29:18.690235	2025-04-13 06:29:18.690237	1
\.


--
-- Data for Name: system_dept; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.system_dept (id, name, "order", parent_id, available, description, created_at, updated_at) FROM stdin;
1	集团总公司	1	\N	t	集团总公司	2025-04-13 06:29:18.661105	2025-04-13 06:29:18.661109
2	西安分公司	1	1	t	西安分公司	2025-04-13 06:29:18.66111	2025-04-13 06:29:18.66111
3	深圳分公司	2	1	t	深圳分公司	2025-04-13 06:29:18.661111	2025-04-13 06:29:18.661111
4	开发组	1	2	t	开发组	2025-04-13 06:29:18.661111	2025-04-13 06:29:18.661112
5	测试组	2	2	t	测试组	2025-04-13 06:29:18.661112	2025-04-13 06:29:18.661112
6	演示组	3	2	t	演示组	2025-04-13 06:29:18.661113	2025-04-13 06:29:18.661113
7	销售部	1	3	t	销售部	2025-04-13 06:29:18.661114	2025-04-13 06:29:18.661114
8	市场部	2	3	t	市场部	2025-04-13 06:29:18.661114	2025-04-13 06:29:18.661115
9	财务部	3	3	t	财务部	2025-04-13 06:29:18.661115	2025-04-13 06:29:18.661115
10	研发部	4	3	t	研发部	2025-04-13 06:29:18.661116	2025-04-13 06:29:18.661116
11	运维部	5	3	t	研发部	2025-04-13 06:29:18.661117	2025-04-13 06:29:18.661117
\.


--
-- Data for Name: system_dict_data; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.system_dict_data (id, dict_sort, dict_label, dict_value, dict_type, css_class, list_class, is_default, available, description, created_at, updated_at, creator_id) FROM stdin;
1	1	男	0	sys_user_sex			t	t	性别男	2025-04-13 06:29:18.696781	2025-04-13 06:29:18.696783	1
2	2	女	1	sys_user_sex			f	t	性别女	2025-04-13 06:29:18.696783	2025-04-13 06:29:18.696784	1
3	3	未知	2	sys_user_sex			f	t	性别未知	2025-04-13 06:29:18.696784	2025-04-13 06:29:18.696785	1
4	4	显示	0	sys_show_hide	btn btn-success btn-xs	primary	t	t	显示菜单	2025-04-13 06:29:18.696785	2025-04-13 06:29:18.696785	1
5	2	隐藏	1	sys_show_hide		danger	f	t	隐藏菜单	2025-04-13 06:29:18.696786	2025-04-13 06:29:18.696786	1
6	1	正常	0	sys_normal_disable		primary	t	t	正常状态	2025-04-13 06:29:18.696787	2025-04-13 06:29:18.696787	1
7	2	停用	1	sys_normal_disable		danger	f	t	停用状态	2025-04-13 06:29:18.696787	2025-04-13 06:29:18.696788	1
8	1	正常	0	sys_job_status		primary	t	t	正常状态	2025-04-13 06:29:18.696788	2025-04-13 06:29:18.696789	1
9	2	暂停	1	sys_job_status		danger	f	t	停用状态	2025-04-13 06:29:18.696789	2025-04-13 06:29:18.696789	1
10	1	默认	default	sys_job_group			t	t	默认分组	2025-04-13 06:29:18.69679	2025-04-13 06:29:18.69679	1
11	2	数据库	sqlalchemy	sys_job_group			f	t	数据库分组	2025-04-13 06:29:18.696791	2025-04-13 06:29:18.696791	1
12	3	redis	redis	sys_job_group			f	t	reids分组	2025-04-13 06:29:18.696791	2025-04-13 06:29:18.696792	1
13	1	默认	default	sys_job_executor			f	t	线程池	2025-04-13 06:29:18.696792	2025-04-13 06:29:18.696792	1
14	2	进程池	processpool	sys_job_executor			f	t	进程池	2025-04-13 06:29:18.696793	2025-04-13 06:29:18.696793	1
15	1	是	Y	sys_yes_no		primary	t	t	系统默认是	2025-04-13 06:29:18.696794	2025-04-13 06:29:18.696794	1
16	2	否	N	sys_yes_no		danger	f	t	系统默认否	2025-04-13 06:29:18.696794	2025-04-13 06:29:18.696795	1
17	1	通知	1	sys_notice_type		warning	t	t	通知	2025-04-13 06:29:18.696795	2025-04-13 06:29:18.696796	1
18	2	公告	2	sys_notice_type		success	f	t	公告	2025-04-13 06:29:18.696796	2025-04-13 06:29:18.696796	1
19	1	正常	0	sys_notice_status		primary	t	t	正常状态	2025-04-13 06:29:18.696797	2025-04-13 06:29:18.696797	1
20	2	关闭	1	sys_notice_status		danger	f	t	关闭状态	2025-04-13 06:29:18.696797	2025-04-13 06:29:18.696798	1
21	99	其他	0	sys_oper_type		info	f	t	其他操作	2025-04-13 06:29:18.696798	2025-04-13 06:29:18.696799	1
22	1	新增	1	sys_oper_type		info	f	t	新增操作	2025-04-13 06:29:18.696799	2025-04-13 06:29:18.696799	1
23	2	修改	2	sys_oper_type		info	f	t	修改操作	2025-04-13 06:29:18.6968	2025-04-13 06:29:18.6968	1
24	3	删除	3	sys_oper_type		danger	f	t	删除操作	2025-04-13 06:29:18.696801	2025-04-13 06:29:18.696801	1
25	4	授权	4	sys_oper_type		primary	f	t	授权操作	2025-04-13 06:29:18.696801	2025-04-13 06:29:18.696802	1
26	5	导出	5	sys_oper_type		warning	f	t	导出操作	2025-04-13 06:29:18.696802	2025-04-13 06:29:18.696802	1
27	6	导入	6	sys_oper_type		warning	f	t	导入操作	2025-04-13 06:29:18.696803	2025-04-13 06:29:18.696803	1
28	7	强退	7	sys_oper_type		danger	f	t	强退操作	2025-04-13 06:29:18.696803	2025-04-13 06:29:18.696804	1
29	8	生成代码	8	sys_oper_type		warning	f	t	生成操作	2025-04-13 06:29:18.696804	2025-04-13 06:29:18.696804	1
30	9	清空数据	9	sys_oper_type		danger	f	t	清空操作	2025-04-13 06:29:18.696805	2025-04-13 06:29:18.696805	1
31	1	成功	0	sys_common_status		primary	f	t	正常状态	2025-04-13 06:29:18.696805	2025-04-13 06:29:18.696806	1
32	2	失败	1	sys_common_status		danger	f	t	停用状态	2025-04-13 06:29:18.696806	2025-04-13 06:29:18.696806	1
\.


--
-- Data for Name: system_dict_type; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.system_dict_type (id, dict_name, dict_type, available, description, created_at, updated_at, creator_id) FROM stdin;
1	用户性别	sys_user_sex	t	用户性别列表	2025-04-13 06:29:18.693001	2025-04-13 06:29:18.693002	1
2	菜单状态	sys_show_hide	t	菜单状态列表	2025-04-13 06:29:18.693003	2025-04-13 06:29:18.693003	1
3	系统开关	sys_normal_disable	t	系统开关列表	2025-04-13 06:29:18.693004	2025-04-13 06:29:18.693004	1
4	任务状态	sys_job_status	t	任务状态列表	2025-04-13 06:29:18.693005	2025-04-13 06:29:18.693005	1
5	任务分组	sys_job_group	t	任务分组列表	2025-04-13 06:29:18.693006	2025-04-13 06:29:18.693006	1
6	任务执行器	sys_job_executor	t	任务执行器列表	2025-04-13 06:29:18.693007	2025-04-13 06:29:18.693007	1
7	系统是否	sys_yes_no	t	系统是否列表	2025-04-13 06:29:18.693008	2025-04-13 06:29:18.693008	1
8	通知类型	sys_notice_type	t	通知类型列表	2025-04-13 06:29:18.693008	2025-04-13 06:29:18.693009	1
9	通知状态	sys_notice_status	t	通知状态列表	2025-04-13 06:29:18.693009	2025-04-13 06:29:18.69301	1
10	操作类型	sys_oper_type	t	操作类型列表	2025-04-13 06:29:18.69301	2025-04-13 06:29:18.69301	1
11	系统状态	sys_common_status	t	登录状态列表	2025-04-13 06:29:18.693011	2025-04-13 06:29:18.693011	1
\.


--
-- Data for Name: system_job; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.system_job (id, name, jobstore, executor, trigger, trigger_args, func, args, kwargs, "coalesce", max_instances, start_date, end_date, status, message, description, created_at, updated_at, creator_id) FROM stdin;
1	系统默认（无参）	default	default	cron	0 0 12 * * ?	scheduler_test.job	\N	\N	f	1	\N	\N	f	\N	\N	2025-04-13 06:29:18.699938	2025-04-13 06:29:18.69994	1
2	系统默认（有参）	default	default	cron	0 0 12 * * ?	scheduler_test.job	test	\N	f	1	\N	\N	f	\N	\N	2025-04-13 06:29:18.69994	2025-04-13 06:29:18.699941	1
3	系统默认（多参）	default	default	cron	0 0 12 * * ?	scheduler_test.job	new	{"test": 111}	f	1	\N	\N	f	\N	\N	2025-04-13 06:29:18.699941	2025-04-13 06:29:18.699942	1
\.


--
-- Data for Name: system_menu; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.system_menu (id, name, type, "order", permission, available, icon, route_name, route_path, component_path, redirect, hidden, cache, parent_id, description, created_at, updated_at) FROM stdin;
1	仪表盘	1	1	dashboard:workplace:query	t	DashboardOutlined	Dashboard	/dashboard	dashboard/workplace	\N	f	t	\N	初始化数据	2025-04-13 06:29:18.668233	2025-04-13 06:29:18.668235
2	系统管理	1	2	\N	t	SettingOutlined	System	/system	\N	/system/menu	f	t	\N	初始化数据	2025-04-13 06:29:18.668236	2025-04-13 06:29:18.668236
3	菜单管理	2	1	system:menu:query	t	\N	Menu	/system/menu	system/menu/index	\N	f	t	2	初始化数据	2025-04-13 06:29:18.668236	2025-04-13 06:29:18.668237
4	部门管理	2	2	system:dept:query	t	\N	Dept	/system/dept	system/dept/index	\N	f	t	2	初始化数据	2025-04-13 06:29:18.668237	2025-04-13 06:29:18.668238
5	岗位管理	2	3	system:position:query	t	\N	Position	/system/position	system/position/index	\N	f	t	2	初始化数据	2025-04-13 06:29:18.668238	2025-04-13 06:29:18.668238
6	角色管理	2	4	system:role:query	t	\N	Role	/system/role	system/role/index	\N	f	t	2	初始化数据	2025-04-13 06:29:18.668239	2025-04-13 06:29:18.668239
7	用户管理	2	5	system:user:query	t	\N	User	/system/user	system/user/index	\N	f	t	2	初始化数据	2025-04-13 06:29:18.668239	2025-04-13 06:29:18.66824
8	日志管理	2	6	system:log:query	t	\N	Log	/system/log	system/log/index	\N	f	t	2	初始化数据	2025-04-13 06:29:18.66824	2025-04-13 06:29:18.668241
9	创建菜单	3	1	system:menu:create	t	\N	\N	\N	\N	\N	f	t	3	初始化数据	2025-04-13 06:29:18.668241	2025-04-13 06:29:18.668241
10	修改菜单	3	2	system:menu:update	t	\N	\N	\N	\N	\N	f	t	3	初始化数据	2025-04-13 06:29:18.668242	2025-04-13 06:29:18.668242
11	删除菜单	3	3	system:menu:delete	t	\N	\N	\N	\N	\N	f	t	3	初始化数据	2025-04-13 06:29:18.668243	2025-04-13 06:29:18.668243
12	批量修改菜单状态	3	4	system:menu:patch	t	\N	\N	\N	\N	\N	f	t	3	初始化数据	2025-04-13 06:29:18.668243	2025-04-13 06:29:18.668244
13	创建部门	3	1	system:dept:create	t	\N	\N	\N	\N	\N	f	t	4	初始化数据	2025-04-13 06:29:18.668244	2025-04-13 06:29:18.668244
14	修改部门	3	2	system:dept:update	t	\N	\N	\N	\N	\N	f	t	4	初始化数据	2025-04-13 06:29:18.668245	2025-04-13 06:29:18.668245
15	删除部门	3	3	system:dept:delete	t	\N	\N	\N	\N	\N	f	t	4	初始化数据	2025-04-13 06:29:18.668246	2025-04-13 06:29:18.668246
16	批量修改部门状态	3	4	system:dept:patch	t	\N	\N	\N	\N	\N	f	t	4	初始化数据	2025-04-13 06:29:18.668246	2025-04-13 06:29:18.668247
17	创建岗位	3	1	system:position:create	t	\N	\N	\N	\N	\N	f	t	5	初始化数据	2025-04-13 06:29:18.668247	2025-04-13 06:29:18.668248
18	修改岗位	3	2	system:position:update	t	\N	\N	\N	\N	\N	f	t	5	初始化数据	2025-04-13 06:29:18.668248	2025-04-13 06:29:18.668248
19	删除岗位	3	3	system:position:delete	t	\N	\N	\N	\N	\N	f	t	5	初始化数据	2025-04-13 06:29:18.668249	2025-04-13 06:29:18.668249
20	批量修改岗位状态	3	4	system:position:patch	t	\N	\N	\N	\N	\N	f	t	5	初始化数据	2025-04-13 06:29:18.668249	2025-04-13 06:29:18.66825
21	岗位导出	3	5	system:position:export	t	\N	\N	\N	\N	\N	f	t	5	初始化数据	2025-04-13 06:29:18.66825	2025-04-13 06:29:18.66825
22	创建角色	3	1	system:role:create	t	\N	\N	\N	\N	\N	f	t	6	初始化数据	2025-04-13 06:29:18.668251	2025-04-13 06:29:18.668251
23	修改角色	3	2	system:role:update	t	\N	\N	\N	\N	\N	f	t	6	初始化数据	2025-04-13 06:29:18.668252	2025-04-13 06:29:18.668252
24	删除角色	3	3	system:role:delete	t	\N	\N	\N	\N	\N	f	t	6	初始化数据	2025-04-13 06:29:18.668252	2025-04-13 06:29:18.668253
25	批量修改角色状态	3	4	system:role:patch	t	\N	\N	\N	\N	\N	f	t	6	初始化数据	2025-04-13 06:29:18.668253	2025-04-13 06:29:18.668253
26	设置角色权限	3	5	system:role:permission	t	\N	\N	\N	\N	\N	f	t	6	初始化数据	2025-04-13 06:29:18.668254	2025-04-13 06:29:18.668254
27	角色导出	3	6	system:role:export	t	\N	\N	\N	\N	\N	f	t	6	初始化数据	2025-04-13 06:29:18.668255	2025-04-13 06:29:18.668255
28	创建用户	3	1	system:user:create	t	\N	\N	\N	\N	\N	f	t	7	初始化数据	2025-04-13 06:29:18.668255	2025-04-13 06:29:18.668256
29	修改用户	3	2	system:user:update	t	\N	\N	\N	\N	\N	f	t	7	初始化数据	2025-04-13 06:29:18.668256	2025-04-13 06:29:18.668256
30	删除用户	3	3	system:user:delete	t	\N	\N	\N	\N	\N	f	t	7	初始化数据	2025-04-13 06:29:18.668257	2025-04-13 06:29:18.668257
31	批量修改用户状态	3	4	system:user:patch	t	\N	\N	\N	\N	\N	f	t	7	初始化数据	2025-04-13 06:29:18.668257	2025-04-13 06:29:18.668258
32	导出用户	3	5	system:user:export	t	\N	\N	\N	\N	\N	f	t	7	初始化数据	2025-04-13 06:29:18.668258	2025-04-13 06:29:18.668259
33	导入用户	3	6	system:user:import	t	\N	\N	\N	\N	\N	f	t	7	初始化数据	2025-04-13 06:29:18.668259	2025-04-13 06:29:18.668259
34	日志删除	3	1	system:operation_log:delete	t	\N	\N	\N	\N	\N	f	t	8	初始化数据	2025-04-13 06:29:18.66826	2025-04-13 06:29:18.66826
35	日志导出	3	2	system:operation_log:export	t	\N	\N	\N	\N	\N	f	t	8	初始化数据	2025-04-13 06:29:18.66826	2025-04-13 06:29:18.668261
36	监控管理	1	3	\N	t	MonitorOutlined	Monitor	/monitor	\N	/monitor/online	f	t	\N	初始化数据	2025-04-13 06:29:18.668261	2025-04-13 06:29:18.668262
37	在线用户	2	1	monitor:online:query	t	\N	MonitorOnline	/monitor/online	monitor/online/index	\N	f	t	36	初始化数据	2025-04-13 06:29:18.668262	2025-04-13 06:29:18.668262
38	在线用户强制下线	3	1	monitor:online:delete	t	\N	\N	\N	\N	\N	f	t	37	初始化数据	2025-04-13 06:29:18.668263	2025-04-13 06:29:18.668263
39	服务器监控	2	2	monitor:server:query	t	\N	MonitorServer	/monitor/server	monitor/server/index	\N	f	t	36	初始化数据	2025-04-13 06:29:18.668263	2025-04-13 06:29:18.668264
40	缓存监控	2	3	monitor:cache:query	t	\N	MonitorCache	/monitor/cache	monitor/cache/index	\N	f	t	36	初始化数据	2025-04-13 06:29:18.668264	2025-04-13 06:29:18.668264
41	清除缓存	3	1	monitor:cache:delete	t	\N	\N	\N	\N	\N	f	t	40	初始化数据	2025-04-13 06:29:18.668265	2025-04-13 06:29:18.668265
42	公共模块	1	4	\N	t	ApiOutlined	Common	/common	\N	/common/docs	f	t	\N	初始化数据	2025-04-13 06:29:18.668266	2025-04-13 06:29:18.668266
43	接口管理	2	1	common:docs:query	t	\N	Docs	/common/docs	common/docs/index	\N	f	t	42	初始化数据	2025-04-13 06:29:18.668266	2025-04-13 06:29:18.668267
44	文档管理	2	2	common:redoc:query	t	\N	Redoc	/common/redoc	common/redoc/index	\N	f	t	42	初始化数据	2025-04-13 06:29:18.668267	2025-04-13 06:29:18.668267
45	公告管理	2	7	system:notice:query	t	\N	Notice	/system/notice	system/notice/index	\N	f	t	2	初始化数据	2025-04-13 06:29:18.668268	2025-04-13 06:29:18.668268
46	公告创建	3	1	system:notice:create	t	\N	\N	\N	\N	\N	f	t	45	初始化数据	2025-04-13 06:29:18.668268	2025-04-13 06:29:18.668269
47	公告修改	3	2	system:notice:update	t	\N	\N	\N	\N	\N	f	t	45	初始化数据	2025-04-13 06:29:18.668269	2025-04-13 06:29:18.66827
48	公告删除	3	3	system:notice:delete	t	\N	\N	\N	\N	\N	f	t	45	初始化数据	2025-04-13 06:29:18.66827	2025-04-13 06:29:18.66827
49	公告导出	3	4	system:notice:export	t	\N	\N	\N	\N	\N	f	t	45	初始化数据	2025-04-13 06:29:18.668271	2025-04-13 06:29:18.668271
50	公告批量修改状态	3	5	system:notice:patch	t	\N	\N	\N	\N	\N	f	t	45	初始化数据	2025-04-13 06:29:18.668271	2025-04-13 06:29:18.668272
51	配置管理	2	8	system:config:query	t	\N	Config	/system/config	system/config/index	\N	f	t	2	初始化数据	2025-04-13 06:29:18.668272	2025-04-13 06:29:18.668272
52	创建配置	3	1	system:config:create	t	\N	\N	\N	\N	\N	f	t	51	初始化数据	2025-04-13 06:29:18.668273	2025-04-13 06:29:18.668273
53	修改配置	3	2	system:config:update	t	\N	\N	\N	\N	\N	f	t	51	初始化数据	2025-04-13 06:29:18.668273	2025-04-13 06:29:18.668274
54	删除配置	3	3	system:config:delete	t	\N	\N	\N	\N	\N	f	t	51	初始化数据	2025-04-13 06:29:18.668274	2025-04-13 06:29:18.668274
55	批量更新配置	3	4	system:config:update	t	\N	\N	\N	\N	\N	f	t	51	初始化数据	2025-04-13 06:29:18.668275	2025-04-13 06:29:18.668275
56	文件上传	3	5	system:config:upload	t	\N	\N	\N	\N	\N	f	t	51	初始化数据	2025-04-13 06:29:18.668276	2025-04-13 06:29:18.668276
57	字典管理	2	9	system:dict_type:query	t	\N	Dict	/system/dict	system/dict/index	\N	f	t	2	初始化数据	2025-04-13 06:29:18.668276	2025-04-13 06:29:18.668277
58	创建字典类型	3	1	system:dict_type:create	t	\N	\N	\N	\N	\N	f	t	57	初始化数据	2025-04-13 06:29:18.668277	2025-04-13 06:29:18.668277
59	修改字典类型	3	2	system:dict_type:update	t	\N	\N	\N	\N	\N	f	t	57	初始化数据	2025-04-13 06:29:18.668278	2025-04-13 06:29:18.668278
60	删除字典类型	3	3	system:dict_type:delete	t	\N	\N	\N	\N	\N	f	t	57	初始化数据	2025-04-13 06:29:18.668278	2025-04-13 06:29:18.668279
61	导出字典类型	3	4	system:dict_type:export	t	\N	\N	\N	\N	\N	f	t	57	初始化数据	2025-04-13 06:29:18.668279	2025-04-13 06:29:18.668279
62	字典数据	2	10	system:dict_data:query	t	\N	DictData	/system/dict_data	system/dict/data	\N	t	t	2	初始化数据	2025-04-13 06:29:18.66828	2025-04-13 06:29:18.66828
63	创建字典数据	3	1	system:dict_data:create	t	\N	\N	\N	\N	\N	f	t	62	初始化数据	2025-04-13 06:29:18.668281	2025-04-13 06:29:18.668281
64	修改字典数据	3	2	system:dict_data:update	t	\N	\N	\N	\N	\N	f	t	62	初始化数据	2025-04-13 06:29:18.668281	2025-04-13 06:29:18.668282
65	删除字典数据	3	3	system:dict_data:delete	t	\N	\N	\N	\N	\N	f	t	62	初始化数据	2025-04-13 06:29:18.668282	2025-04-13 06:29:18.668282
66	导出字典数据	3	4	system:dict_data:export	t	\N	\N	\N	\N	\N	f	t	62	初始化数据	2025-04-13 06:29:18.668283	2025-04-13 06:29:18.668283
67	任务管理	2	11	system:job:query	t	\N	Job	/system/job	system/job/index	\N	f	t	2	初始化数据	2025-04-13 06:29:18.668283	2025-04-13 06:29:18.668284
68	创建任务	3	1	system:job:create	t	\N	\N	\N	\N	\N	f	t	67	初始化数据	2025-04-13 06:29:18.668284	2025-04-13 06:29:18.668284
69	修改和操作任务	3	2	system:job:update	t	\N	\N	\N	\N	\N	f	t	67	初始化数据	2025-04-13 06:29:18.668285	2025-04-13 06:29:18.668285
70	删除和清除任务	3	3	system:job:delete	t	\N	\N	\N	\N	\N	f	t	67	初始化数据	2025-04-13 06:29:18.668285	2025-04-13 06:29:18.668286
71	导出定时任务	3	4	system:job:export	t	\N	\N	\N	\N	\N	f	t	67	初始化数据	2025-04-13 06:29:18.668286	2025-04-13 06:29:18.668286
\.


--
-- Data for Name: system_notice; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.system_notice (id, notice_title, notice_type, notice_content, available, description, created_at, updated_at, creator_id) FROM stdin;
1	系统更新	1	2099年9月9日，晚上12:00，系统更新	t	系统更新	2025-04-13 06:29:18.687866	2025-04-13 06:29:18.687867	1
2	系统维护	2	2099年9月9日，晚上12:00，系统维护	t	系统维护	2025-04-13 06:29:18.687868	2025-04-13 06:29:18.687868	1
3	系统更新完成	1	2099年9月9日，晚上12:00，系统更新完成	f	系统更新完成	2025-04-13 06:29:18.687868	2025-04-13 06:29:18.687869	1
4	系统维护完成	2	2099年9月9日，晚上12:00，系统维护完成	f	系统维护完成	2025-04-13 06:29:18.687869	2025-04-13 06:29:18.68787	1
\.


--
-- Data for Name: system_operation_log; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.system_operation_log (id, request_path, request_method, request_payload, request_ip, request_os, request_browser, response_code, response_json, description, created_at, updated_at, creator_id) FROM stdin;
\.


--
-- Data for Name: system_position; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.system_position (id, name, "order", available, description, created_at, updated_at, creator_id) FROM stdin;
1	董事长岗	1	t	董事长岗位	2025-04-13 06:29:18.674788	2025-04-13 06:29:18.674789	1
2	运营岗	2	t	运营岗位	2025-04-13 06:29:18.67479	2025-04-13 06:29:18.67479	1
3	销售岗	3	t	销售岗	2025-04-13 06:29:18.67479	2025-04-13 06:29:18.674791	1
4	人事行政岗	4	t	人事行政岗	2025-04-13 06:29:18.674791	2025-04-13 06:29:18.674791	1
5	开发岗	5	t	开发岗	2025-04-13 06:29:18.674792	2025-04-13 06:29:18.674792	1
6	测试岗	6	t	测试岗	2025-04-13 06:29:18.674793	2025-04-13 06:29:18.674793	1
7	演示岗	7	t	演示岗	2025-04-13 06:29:18.674793	2025-04-13 06:29:18.674794	1
\.


--
-- Data for Name: system_role; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.system_role (id, name, "order", data_scope, available, description, created_at, updated_at, creator_id) FROM stdin;
1	管理员角色	1	4	t	管理员	2025-04-13 06:29:18.678555	2025-04-13 06:29:18.678556	1
2	演示角色	2	5	t	演示角色	2025-04-13 06:29:18.678557	2025-04-13 06:29:18.678557	1
\.


--
-- Data for Name: system_role_depts; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.system_role_depts (role_id, dept_id) FROM stdin;
1	1
2	1
2	6
\.


--
-- Data for Name: system_role_menus; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.system_role_menus (role_id, menu_id) FROM stdin;
1	1
1	2
1	3
1	4
1	5
1	6
1	7
1	8
1	9
1	10
1	11
1	12
1	13
1	14
1	15
1	16
1	17
1	18
1	19
1	20
1	21
1	22
1	23
1	24
1	25
1	26
1	27
1	28
1	29
1	30
1	31
1	32
1	33
1	34
1	35
1	36
1	37
1	38
1	39
1	40
1	41
1	42
1	43
1	44
1	45
1	46
1	47
1	48
1	49
1	50
1	51
1	52
1	53
1	54
1	55
1	56
1	57
1	58
1	59
1	60
1	61
1	62
1	63
1	64
1	65
1	66
1	67
1	68
1	69
1	70
1	71
2	1
2	2
2	3
\.


--
-- Data for Name: system_user_positions; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.system_user_positions (user_id, position_id) FROM stdin;
1	5
2	7
\.


--
-- Data for Name: system_user_roles; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.system_user_roles (user_id, role_id) FROM stdin;
1	1
2	2
\.


--
-- Data for Name: system_users; Type: TABLE DATA; Schema: public; Owner: tao
--

COPY public.system_users (id, username, password, name, mobile, email, gender, avatar, available, is_superuser, last_login, dept_id, description, created_at, updated_at, creator_id) FROM stdin;
1	admin	$2b$12$e2IJgS/cvHgJ0H3G7Xa08OXoXnk6N/NX3IZRtubBDElA0VLZhkNOa	管理员	15382112222	admin@qq.com	1	https://gw.alipayobjects.com/zos/rmsportal/BiazfanxmamNRoxxVxka.png	t	t	\N	1	超级管理员	2025-04-13 06:29:18.672554	2025-04-13 06:29:18.672558	\N
2	demo	$2b$12$e2IJgS/cvHgJ0H3G7Xa08OXoXnk6N/NX3IZRtubBDElA0VLZhkNOa	演示用户	15382112121	demo@qq.com	1	https://gw.alipayobjects.com/zos/rmsportal/BiazfanxmamNRoxxVxka.png	t	f	\N	6	演示用户	2025-04-13 06:29:18.672559	2025-04-13 06:29:18.672559	1
\.


--
-- Name: system_config_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.system_config_id_seq', 1, false);


--
-- Name: system_dept_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.system_dept_id_seq', 1, false);


--
-- Name: system_dict_data_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.system_dict_data_id_seq', 1, false);


--
-- Name: system_dict_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.system_dict_type_id_seq', 1, false);


--
-- Name: system_job_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.system_job_id_seq', 1, false);


--
-- Name: system_menu_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.system_menu_id_seq', 1, false);


--
-- Name: system_notice_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.system_notice_id_seq', 1, false);


--
-- Name: system_operation_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.system_operation_log_id_seq', 1, false);


--
-- Name: system_position_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.system_position_id_seq', 1, false);


--
-- Name: system_role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.system_role_id_seq', 1, false);


--
-- Name: system_users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tao
--

SELECT pg_catalog.setval('public.system_users_id_seq', 1, false);


--
-- Name: system_config system_config_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_config
    ADD CONSTRAINT system_config_pkey PRIMARY KEY (id);


--
-- Name: system_dept system_dept_name_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_dept
    ADD CONSTRAINT system_dept_name_key UNIQUE (name);


--
-- Name: system_dept system_dept_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_dept
    ADD CONSTRAINT system_dept_pkey PRIMARY KEY (id);


--
-- Name: system_dict_data system_dict_data_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_dict_data
    ADD CONSTRAINT system_dict_data_pkey PRIMARY KEY (id);


--
-- Name: system_dict_type system_dict_type_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_dict_type
    ADD CONSTRAINT system_dict_type_pkey PRIMARY KEY (id);


--
-- Name: system_job system_job_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_job
    ADD CONSTRAINT system_job_pkey PRIMARY KEY (id);


--
-- Name: system_menu system_menu_name_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_menu
    ADD CONSTRAINT system_menu_name_key UNIQUE (name);


--
-- Name: system_menu system_menu_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_menu
    ADD CONSTRAINT system_menu_pkey PRIMARY KEY (id);


--
-- Name: system_notice system_notice_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_notice
    ADD CONSTRAINT system_notice_pkey PRIMARY KEY (id);


--
-- Name: system_operation_log system_operation_log_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_operation_log
    ADD CONSTRAINT system_operation_log_pkey PRIMARY KEY (id);


--
-- Name: system_position system_position_name_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_position
    ADD CONSTRAINT system_position_name_key UNIQUE (name);


--
-- Name: system_position system_position_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_position
    ADD CONSTRAINT system_position_pkey PRIMARY KEY (id);


--
-- Name: system_role_depts system_role_depts_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_role_depts
    ADD CONSTRAINT system_role_depts_pkey PRIMARY KEY (role_id, dept_id);


--
-- Name: system_role_menus system_role_menus_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_role_menus
    ADD CONSTRAINT system_role_menus_pkey PRIMARY KEY (role_id, menu_id);


--
-- Name: system_role system_role_name_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_role
    ADD CONSTRAINT system_role_name_key UNIQUE (name);


--
-- Name: system_role system_role_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_role
    ADD CONSTRAINT system_role_pkey PRIMARY KEY (id);


--
-- Name: system_user_positions system_user_positions_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_user_positions
    ADD CONSTRAINT system_user_positions_pkey PRIMARY KEY (user_id, position_id);


--
-- Name: system_user_roles system_user_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_user_roles
    ADD CONSTRAINT system_user_roles_pkey PRIMARY KEY (user_id, role_id);


--
-- Name: system_users system_users_pkey; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_users
    ADD CONSTRAINT system_users_pkey PRIMARY KEY (id);


--
-- Name: system_users system_users_username_key; Type: CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_users
    ADD CONSTRAINT system_users_username_key UNIQUE (username);


--
-- Name: ix_system_config_creator_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_system_config_creator_id ON public.system_config USING btree (creator_id);


--
-- Name: ix_system_dept_parent_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_system_dept_parent_id ON public.system_dept USING btree (parent_id);


--
-- Name: ix_system_dict_data_creator_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_system_dict_data_creator_id ON public.system_dict_data USING btree (creator_id);


--
-- Name: ix_system_dict_type_creator_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_system_dict_type_creator_id ON public.system_dict_type USING btree (creator_id);


--
-- Name: ix_system_job_creator_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_system_job_creator_id ON public.system_job USING btree (creator_id);


--
-- Name: ix_system_menu_parent_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_system_menu_parent_id ON public.system_menu USING btree (parent_id);


--
-- Name: ix_system_notice_creator_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_system_notice_creator_id ON public.system_notice USING btree (creator_id);


--
-- Name: ix_system_operation_log_creator_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_system_operation_log_creator_id ON public.system_operation_log USING btree (creator_id);


--
-- Name: ix_system_operation_log_request_method; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_system_operation_log_request_method ON public.system_operation_log USING btree (request_method);


--
-- Name: ix_system_operation_log_request_path; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_system_operation_log_request_path ON public.system_operation_log USING btree (request_path);


--
-- Name: ix_system_position_creator_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_system_position_creator_id ON public.system_position USING btree (creator_id);


--
-- Name: ix_system_role_creator_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_system_role_creator_id ON public.system_role USING btree (creator_id);


--
-- Name: ix_system_role_depts_dept_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_system_role_depts_dept_id ON public.system_role_depts USING btree (dept_id);


--
-- Name: ix_system_role_depts_role_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_system_role_depts_role_id ON public.system_role_depts USING btree (role_id);


--
-- Name: ix_system_role_menus_menu_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_system_role_menus_menu_id ON public.system_role_menus USING btree (menu_id);


--
-- Name: ix_system_role_menus_role_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_system_role_menus_role_id ON public.system_role_menus USING btree (role_id);


--
-- Name: ix_system_user_positions_position_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_system_user_positions_position_id ON public.system_user_positions USING btree (position_id);


--
-- Name: ix_system_user_positions_user_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_system_user_positions_user_id ON public.system_user_positions USING btree (user_id);


--
-- Name: ix_system_user_roles_role_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_system_user_roles_role_id ON public.system_user_roles USING btree (role_id);


--
-- Name: ix_system_user_roles_user_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_system_user_roles_user_id ON public.system_user_roles USING btree (user_id);


--
-- Name: ix_system_users_creator_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_system_users_creator_id ON public.system_users USING btree (creator_id);


--
-- Name: ix_system_users_dept_id; Type: INDEX; Schema: public; Owner: tao
--

CREATE INDEX ix_system_users_dept_id ON public.system_users USING btree (dept_id);


--
-- Name: system_config system_config_creator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_config
    ADD CONSTRAINT system_config_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES public.system_users(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: system_dept system_dept_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_dept
    ADD CONSTRAINT system_dept_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.system_dept(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: system_dict_data system_dict_data_creator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_dict_data
    ADD CONSTRAINT system_dict_data_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES public.system_users(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: system_dict_type system_dict_type_creator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_dict_type
    ADD CONSTRAINT system_dict_type_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES public.system_users(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: system_job system_job_creator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_job
    ADD CONSTRAINT system_job_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES public.system_users(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: system_menu system_menu_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_menu
    ADD CONSTRAINT system_menu_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.system_menu(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: system_notice system_notice_creator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_notice
    ADD CONSTRAINT system_notice_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES public.system_users(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: system_operation_log system_operation_log_creator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_operation_log
    ADD CONSTRAINT system_operation_log_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES public.system_users(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: system_position system_position_creator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_position
    ADD CONSTRAINT system_position_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES public.system_users(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: system_role system_role_creator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_role
    ADD CONSTRAINT system_role_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES public.system_users(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: system_role_depts system_role_depts_dept_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_role_depts
    ADD CONSTRAINT system_role_depts_dept_id_fkey FOREIGN KEY (dept_id) REFERENCES public.system_dept(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: system_role_depts system_role_depts_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_role_depts
    ADD CONSTRAINT system_role_depts_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.system_role(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: system_role_menus system_role_menus_menu_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_role_menus
    ADD CONSTRAINT system_role_menus_menu_id_fkey FOREIGN KEY (menu_id) REFERENCES public.system_menu(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: system_role_menus system_role_menus_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_role_menus
    ADD CONSTRAINT system_role_menus_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.system_role(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: system_user_positions system_user_positions_position_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_user_positions
    ADD CONSTRAINT system_user_positions_position_id_fkey FOREIGN KEY (position_id) REFERENCES public.system_position(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: system_user_positions system_user_positions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_user_positions
    ADD CONSTRAINT system_user_positions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.system_users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: system_user_roles system_user_roles_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_user_roles
    ADD CONSTRAINT system_user_roles_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.system_role(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: system_user_roles system_user_roles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_user_roles
    ADD CONSTRAINT system_user_roles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.system_users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: system_users system_users_creator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_users
    ADD CONSTRAINT system_users_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES public.system_users(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: system_users system_users_dept_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tao
--

ALTER TABLE ONLY public.system_users
    ADD CONSTRAINT system_users_dept_id_fkey FOREIGN KEY (dept_id) REFERENCES public.system_dept(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- PostgreSQL database dump complete
--

